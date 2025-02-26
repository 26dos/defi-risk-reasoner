"""Top-level entrypoint for the risk reasoner."""
import os

from .llm.client import LLMClient
from .llm.agent import Agent
from .prompts import SYSTEM_RISK_ANALYST
from .tools.registry import TOOL_DEFINITIONS, build_handlers


def analyze_position(user_address: str, rpc_url: str = None,
                     model: str = None, max_iterations: int = 12) -> dict:
    rpc_url = rpc_url or os.environ["ETH_RPC_URL"]
    client_kwargs = {}
    if model:
        client_kwargs["model"] = model
    client = LLMClient(**client_kwargs)
    agent = Agent(
        client=client,
        system=SYSTEM_RISK_ANALYST,
        tools=TOOL_DEFINITIONS,
        handlers=build_handlers(rpc_url),
        max_iterations=max_iterations,
    )
    user_msg = (
        f"Please produce a risk report for the wallet {user_address}.\n"
        f"Focus on Aave V3 positions on Ethereum mainnet."
    )
    return agent.run(user_msg)
