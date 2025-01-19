"""Pull recent governance proposals for a protocol and summarize them.

We use the Snapshot Hub graphql API for off-chain governance and
governor-bravo style on-chain governance for the rest. The output is
intentionally minimal — the LLM gets a compact summary, not raw proposals.
"""
import requests


SNAPSHOT_API = "https://hub.snapshot.org/graphql"


def fetch_snapshot_proposals(space_id: str, limit: int = 10):
    query = """
    query Proposals($space: String!, $limit: Int!) {
      proposals(first: $limit, where: {space: $space}, orderBy: "created", orderDirection: desc) {
        id title state created end scores_total
      }
    }
    """
    r = requests.post(
        SNAPSHOT_API,
        json={"query": query, "variables": {"space": space_id, "limit": limit}},
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("data", {}).get("proposals", [])
