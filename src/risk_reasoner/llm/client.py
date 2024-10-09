"""Wrapper around the Anthropic SDK."""
import os
from typing import Any

from anthropic import Anthropic


DEFAULT_MODEL = "claude-sonnet-4-5"


class LLMClient:
    def __init__(self, api_key=None, model=DEFAULT_MODEL):
        self.client = Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def message(self, system, messages, tools=None, max_tokens=4096,
                cache_system: bool = True, cache_tools: bool = True):
        """Call the messages API with optional prompt caching.

        We cache the system prompt and tool definitions because they are
        large (especially tools) and they don't change across an agent run.
        That alone usually pays for itself within ~3 turns.
        """
        # mark the system prompt as cacheable
        if cache_system and isinstance(system, str):
            system = [{"type": "text", "text": system,
                       "cache_control": {"type": "ephemeral"}}]
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools is not None:
            if cache_tools and tools:
                tools = list(tools)
                tools[-1] = {**tools[-1], "cache_control": {"type": "ephemeral"}}
            kwargs["tools"] = tools
        return self.client.messages.create(**kwargs)


def quick_ask(prompt: str, system: str = "You are a helpful assistant.") -> str:
    client = LLMClient()
    msg = client.message(system=system, messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")
