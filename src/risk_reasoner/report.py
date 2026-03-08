"""Render the agent's final response into a human-readable report."""
from typing import Any


def _block_attr(b, name, default=None):
    if isinstance(b, dict):
        return b.get(name, default)
    return getattr(b, name, default)


def extract_final_text(run_result: dict) -> str:
    for m in reversed(run_result["messages"]):
        if m["role"] != "assistant":
            continue
        parts = []
        for b in m["content"]:
            text = _block_attr(b, "text")
            if text:
                parts.append(text)
        if parts:
            return "\n".join(parts)
    return "(no report generated)"


def tool_call_log(run_result: dict) -> list[dict]:
    log = []
    for m in run_result["messages"]:
        if m["role"] != "assistant":
            continue
        for b in m["content"]:
            if _block_attr(b, "type") != "tool_use":
                continue
            log.append({
                "tool": _block_attr(b, "name"),
                "input": _block_attr(b, "input") or {},
            })
    return log


def usage_summary(run_result: dict) -> dict:
    u = run_result.get("usage") or {}
    cached = u.get("cache_read_input_tokens", 0) or 0
    fresh = u.get("input_tokens", 0) or 0
    out = u.get("output_tokens", 0) or 0
    return {
        "input_tokens": fresh,
        "output_tokens": out,
        "cache_read_tokens": cached,
        "cache_hit_ratio": (cached / max(1, fresh + cached)),
    }


def render_terminal(run_result: dict) -> None:
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

    u = usage_summary(run_result)
    console.print(
        f"\n[dim]tokens: {u['input_tokens']} in / {u['output_tokens']} out, "
        f"cache hit: {u['cache_hit_ratio']*100:.0f}%[/dim]"
    )
