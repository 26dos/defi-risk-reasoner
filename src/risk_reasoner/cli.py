"""defi-risk-reasoner — command line entrypoint."""
import os
import sys

import click


@click.group()
@click.version_option()
def cli():
    """DeFi Risk Reasoner — analyze positions with an LLM agent."""


@cli.command("analyze")
@click.argument("wallet")
@click.option("--rpc", default=None, help="Ethereum RPC (overrides ETH_RPC_URL)")
@click.option("--model", default=None)
@click.option("--max-iterations", type=int, default=12)
@click.option("--out", default=None, help="write final report to a file")
def analyze_cmd(wallet, rpc, model, max_iterations, out):
    """Produce a risk report for WALLET."""
    from .runner import analyze_position
    from .report import render_terminal, extract_final_text

    result = analyze_position(
        wallet, rpc_url=rpc, model=model, max_iterations=max_iterations,
    )
    render_terminal(result)
    if out:
        with open(out, "w") as f:
            f.write(extract_final_text(result))
        click.echo(f"\nwrote -> {out}")


@cli.command("quick")
@click.argument("question")
def quick_cmd(question):
    """One-shot LLM query for ad-hoc DeFi questions."""
    from .llm.client import quick_ask
    click.echo(quick_ask(question, system="You are a DeFi expert."))


if __name__ == "__main__":
    cli()
