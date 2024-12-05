"""Heuristics for flagging risky oracle configurations.

These rules come from post-mortems of past DeFi exploits — they are NOT
exhaustive, and a passing audit is not a guarantee.
"""

# Aggregator descriptions that are known to back protocols with a history of
# oracle-manipulation incidents.
KNOWN_HIGH_RISK_FEEDS = {
    # Specific feeds that have had stale-price issues in past incidents
    # (kept here as a starting point for new analyses)
    "0xab44ed03d3d3aaaa": "stale-prone deprecated feed",
}


def assess_chainlink_feed(feed: dict, max_staleness_seconds: int = 24 * 3600):
    findings = []
    if feed["staleness_seconds"] > max_staleness_seconds:
        findings.append({
            "severity": "high",
            "rule": "chainlink_stale",
            "detail": f"feed last updated {feed['staleness_seconds']}s ago, "
                      f"threshold is {max_staleness_seconds}s",
        })
    if feed["round_id"] != feed["answered_in_round"]:
        findings.append({
            "severity": "medium",
            "rule": "chainlink_round_mismatch",
            "detail": "round_id != answered_in_round",
        })
    if feed["answer"] <= 0:
        findings.append({
            "severity": "high",
            "rule": "chainlink_nonpositive",
            "detail": "feed returned non-positive answer",
        })
    if feed["aggregator"].lower() in KNOWN_HIGH_RISK_FEEDS:
        findings.append({
            "severity": "high",
            "rule": "known_high_risk_feed",
            "detail": KNOWN_HIGH_RISK_FEEDS[feed["aggregator"].lower()],
        })
    return findings
