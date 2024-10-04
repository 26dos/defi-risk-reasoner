"""A minimal tool-using agent loop on top of the Anthropic API.

The agent runs until the model returns an `end_turn` stop reason or until
`max_iterations` is reached. Each tool_use block is dispatched to the
registered tool handler and the result is passed back as a tool_result.
"""
from typing import Any, Callable

from .client import LLMClient


class ToolError(Exception):
    pass


class Agent:
    def __init__(self, client: LLMClient, system: str, tools: list[dict],
                 handlers: dict[str, Callable[[dict], Any]],
                 max_iterations: int = 12):
        self.client = client
        self.system = system
        self.tools = tools
        self.handlers = handlers
        self.max_iterations = max_iterations

    def run(self, user_message: str) -> dict:
        messages = [{"role": "user", "content": user_message}]
        for step in range(self.max_iterations):
            response = self.client.message(
                system=self.system,
                messages=messages,
                tools=self.tools,
            )
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                return {"messages": messages, "steps": step + 1}

            tool_uses = [b for b in response.content if b.type == "tool_use"]
            if not tool_uses:
                return {"messages": messages, "steps": step + 1}

            results = []
            for tu in tool_uses:
                handler = self.handlers.get(tu.name)
                try:
                    if handler is None:
                        raise ToolError(f"unknown tool: {tu.name}")
                    output = handler(tu.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": output if isinstance(output, str) else str(output),
                    })
                except Exception as e:
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": f"error: {e}",
                        "is_error": True,
                    })
            messages.append({"role": "user", "content": results})
        return {"messages": messages, "steps": self.max_iterations, "exhausted": True}
