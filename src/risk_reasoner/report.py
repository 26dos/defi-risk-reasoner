"""Render the agent's final response into a human-readable report."""
from typing import Any


def extract_final_text(run_result: dict) -> str:
    """The last assistant message is the rendered report."""
    for m in reversed(run_result["messages"]):
        if m["role"] != "assistant":
            continue
        # content is a list of typed blocks
        parts = []
        for b in m["content"]:
            text = getattr(b, "text", None) if not isinstance(b, dict) else b.get("text")
            if text:
                parts.append(text)
        if parts:
            return "\n".join(parts)
    return "(no report generated)"


def tool_call_log(run_result: dict) -> list[dict]:
    """Return a flat log of tool calls made during the run."""
    log = []
    for m in run_result["messages"]:
        if m["role"] != "assistant":
            continue
        for b in m["content"]:
            tname = getattr(b, "name", None) if not isinstance(b, dict) else b.get("name")
            if tname and getattr(b, "type", None) == "tool_use":
                log.append({"tool": tname,
                            "input": getattr(b, "input", {}) or b.get("input", {})})
    return log
