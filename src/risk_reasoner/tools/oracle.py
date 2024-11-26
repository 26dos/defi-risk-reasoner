"""Inspect price feeds backing a position.

We support Chainlink as the canonical reference. Custom oracles (e.g.,
single-source TWAPs) are flagged separately because they're a known
exploitation vector.
"""
import time

from web3 import Web3


CHAINLINK_AGGREGATOR_ABI = [
    {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "type": "function"},
    {"inputs": [], "name": "description", "outputs": [{"type": "string"}], "type": "function"},
    {"inputs": [], "name": "latestRoundData",
     "outputs": [
         {"name": "roundId", "type": "uint80"},
         {"name": "answer", "type": "int256"},
         {"name": "startedAt", "type": "uint256"},
         {"name": "updatedAt", "type": "uint256"},
         {"name": "answeredInRound", "type": "uint80"},
     ],
     "type": "function"},
]


def fetch_chainlink_feed(rpc_url: str, aggregator: str):
    """Return latest answer + staleness."""
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(aggregator),
                        abi=CHAINLINK_AGGREGATOR_ABI)
    decimals = c.functions.decimals().call()
    desc = c.functions.description().call()
    rid, answer, started, updated, ans_round = c.functions.latestRoundData().call()
    now = int(time.time())
    return {
        "aggregator": aggregator,
        "description": desc,
        "decimals": int(decimals),
        "answer": int(answer),
        "answer_human": int(answer) / (10 ** int(decimals)),
        "updated_at": int(updated),
        "staleness_seconds": now - int(updated),
        "round_id": int(rid),
        "answered_in_round": int(ans_round),
    }



def feed_drift(feed_a: dict, feed_b: dict) -> dict:
    """Compare two feeds priced in the same denomination.

    Useful when one protocol uses one feed and another uses a different feed
    for the same asset — drift between them is an arbitrage / liquidation
    surface.
    """
    a = feed_a["answer_human"]
    b = feed_b["answer_human"]
    if a == 0 or b == 0:
        return {"drift_bps": None, "diff_abs": abs(a - b)}
    bps = abs(a - b) / max(a, b) * 10_000
    return {"drift_bps": bps, "feed_a": a, "feed_b": b}
