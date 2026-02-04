"""Wrapper around the Anthropic SDK."""
import os

from anthropic import Anthropic


# Switched to 4.6 for the slightly better tool-use behavior in long traces.
DEFAULT_MODEL = "claude-sonnet-4-6"


class LLMClient:
    def __init__(self, api_key=None, model=DEFAULT_MODEL):
        self.client = Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def message(self, system, messages, tools=None, max_tokens=4096,
                cache_system: bool = True, cache_tools: bool = True):
        if cache_system and isinstance(system, str):
            system = [{
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }]
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools is not None:
            if cache_tools and tools:
                tools = [{**t} for t in tools]
                tools[-1]["cache_control"] = {"type": "ephemeral"}
            kwargs["tools"] = tools
        return self.client.messages.create(**kwargs)


def quick_ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    client = LLMClient()
    msg = client.message(system=system, messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")
