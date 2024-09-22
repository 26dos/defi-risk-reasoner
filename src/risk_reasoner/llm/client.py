"""Wrapper around the Anthropic SDK.

We isolate the SDK behind this module so that tests can stub it out and so
that we have one place to plug in retries, logging, and (later) prompt
caching.
"""
import os
from typing import Any

from anthropic import Anthropic


DEFAULT_MODEL = "claude-sonnet-4-5"


class LLMClient:
    def __init__(self, api_key=None, model=DEFAULT_MODEL):
        self.client = Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def message(self, system, messages, tools=None, max_tokens=4096):
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools is not None:
            kwargs["tools"] = tools
        return self.client.messages.create(**kwargs)
