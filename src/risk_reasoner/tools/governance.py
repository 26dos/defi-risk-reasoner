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



def assess_proposals(proposals: list[dict]) -> list[dict]:
    """Surface proposals that are near-term and potentially impactful."""
    findings = []
    for p in proposals:
        duration = (p.get("end") or 0) - (p.get("created") or 0)
        if p.get("state") == "active" and duration > 0 and duration < 24 * 3600:
            findings.append({
                "severity": "medium",
                "rule": "short_voting_window",
                "proposal_id": p["id"],
                "detail": f"voting window is {duration // 3600}h ({p.get('title')})",
            })
        if p.get("scores_total", 0) == 0 and p.get("state") == "active":
            findings.append({
                "severity": "low",
                "rule": "low_participation",
                "proposal_id": p["id"],
                "detail": "no votes yet on an active proposal",
            })
    return findings
