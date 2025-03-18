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



def render_terminal(run_result: dict) -> None:
    """Pretty-print a report to the terminal."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.table import Table

    console = Console()
    console.print(Panel.fit("DeFi Risk Reasoner — report", style="bold cyan"))
    console.print(Markdown(extract_final_text(run_result)))

    log = tool_call_log(run_result)
    if log:
        t = Table(title="Tool calls", show_lines=False)
        t.add_column("#")
        t.add_column("Tool")
        t.add_column("Input")
        for i, c in enumerate(log, 1):
            t.add_row(str(i), c["tool"], str(c["input"])[:100])
        console.print(t)
