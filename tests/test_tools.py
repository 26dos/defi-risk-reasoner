import pytest

from risk_reasoner.tools import registry as reg


def test_every_tool_has_handler(monkeypatch):
    monkeypatch.setenv("ETH_RPC_URL", "http://localhost:8545")
    handlers = reg.build_handlers("http://localhost:8545")
    tool_names = {t["name"] for t in reg.TOOL_DEFINITIONS}
    handler_names = set(handlers.keys())
    assert tool_names == handler_names


def test_tool_input_schemas_have_required_fields():
    for t in reg.TOOL_DEFINITIONS:
        assert "name" in t
        assert "description" in t
        assert "input_schema" in t
        assert t["input_schema"]["type"] == "object"
