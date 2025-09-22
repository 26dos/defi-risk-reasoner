"""Test the tool-use loop without hitting the real Anthropic API."""
from types import SimpleNamespace

from risk_reasoner.llm.agent import Agent


class MockClient:
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def message(self, system, messages, tools=None, **kwargs):
        self.calls += 1
        return self._responses.pop(0)


def _resp(content_blocks, stop_reason="end_turn"):
    return SimpleNamespace(
        content=content_blocks,
        stop_reason=stop_reason,
        usage=SimpleNamespace(
            input_tokens=10,
            output_tokens=5,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
        ),
    )


def _text_block(text):
    return SimpleNamespace(type="text", text=text)


def _tool_use(name, inp, id):
    return SimpleNamespace(type="tool_use", name=name, input=inp, id=id)


def test_agent_returns_text_on_end_turn():
    client = MockClient([_resp([_text_block("done.")])])
    agent = Agent(client=client, system="sys", tools=[], handlers={})
    out = agent.run("hi")
    assert out["steps"] == 1
    assert out["stop_reason"] == "end_turn"


def test_agent_dispatches_tool_then_finishes():
    seen = []
    client = MockClient([
        _resp([_tool_use("ping", {"x": 1}, "abc")], stop_reason="tool_use"),
        _resp([_text_block("answered.")]),
    ])
    handlers = {"ping": lambda inp: seen.append(inp) or "pong"}
    agent = Agent(client=client, system="sys",
                  tools=[{"name": "ping", "description": "p",
                          "input_schema": {"type": "object", "properties": {}}}],
                  handlers=handlers)
    out = agent.run("ping it")
    assert out["steps"] == 2
    assert seen == [{"x": 1}]


def test_agent_handles_unknown_tool_gracefully():
    client = MockClient([
        _resp([_tool_use("nope", {}, "id1")], stop_reason="tool_use"),
        _resp([_text_block("ok.")]),
    ])
    agent = Agent(client=client, system="sys", tools=[], handlers={})
    out = agent.run("go")
    # we expect the loop to continue past the tool failure
    assert out["steps"] == 2
