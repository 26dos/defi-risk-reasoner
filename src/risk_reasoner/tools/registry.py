"""Tool definitions exposed to the LLM agent.

Each entry follows Anthropic's tool schema. The handlers wrap the underlying
implementations with consistent argument names so the model sees a uniform
interface.
"""
from . import aave, oracle, oracle_audit, scenarios, governance, erc20


TOOL_DEFINITIONS = [
    {
        "name": "fetch_aave_v3_summary",
        "description": "Get a user's aggregate Aave V3 position state on Ethereum mainnet (collateral, debt, health factor, liquidation threshold).",
        "input_schema": {
            "type": "object",
            "properties": {
                "user": {"type": "string", "description": "wallet address (0x-prefixed)"},
            },
            "required": ["user"],
        },
    },
    {
        "name": "fetch_chainlink_feed",
        "description": "Read the latest price from a Chainlink aggregator and report staleness.",
        "input_schema": {
            "type": "object",
            "properties": {
                "aggregator": {"type": "string", "description": "aggregator address"},
            },
            "required": ["aggregator"],
        },
    },
    {
        "name": "stress_position",
        "description": "Project the user's health factor under a set of pre-defined price stress scenarios.",
        "input_schema": {
            "type": "object",
            "properties": {
                "collateral_value_usd": {"type": "number"},
                "debt_value_usd": {"type": "number"},
                "liquidation_threshold_bps": {"type": "integer"},
            },
            "required": ["collateral_value_usd", "debt_value_usd", "liquidation_threshold_bps"],
        },
    },
    {
        "name": "fetch_governance_proposals",
        "description": "Recent proposals from a Snapshot space.",
        "input_schema": {
            "type": "object",
            "properties": {
                "space_id": {"type": "string", "description": "snapshot space id, e.g. 'aave.eth'"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["space_id"],
        },
    },
]


def build_handlers(rpc_url: str):
    return {
        "fetch_aave_v3_summary": lambda inp: aave.fetch_aave_v3_summary(rpc_url, inp["user"]),
        "fetch_chainlink_feed": lambda inp: oracle.fetch_chainlink_feed(rpc_url, inp["aggregator"]),
        "stress_position": lambda inp: scenarios.run_scenarios(
            inp["collateral_value_usd"], inp["debt_value_usd"], inp["liquidation_threshold_bps"],
        ),
        "fetch_governance_proposals": lambda inp: governance.fetch_snapshot_proposals(
            inp["space_id"], inp.get("limit", 10),
        ),
    }
