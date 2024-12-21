"""Pre-baked stress scenarios applied to a position."""
from .liquidation import project_health_factor


SCENARIOS = [
    {"name": "eth_-20%", "collateral_change_pct": -20.0},
    {"name": "eth_-30%", "collateral_change_pct": -30.0},
    {"name": "eth_-50%", "collateral_change_pct": -50.0},
    {"name": "stablecoin_depeg_-10%", "debt_change_pct": -10.0},
    {"name": "stablecoin_depeg_+5%", "debt_change_pct": 5.0},
]


def run_scenarios(collateral_value_usd, debt_value_usd, liq_threshold_bps):
    out = []
    for s in SCENARIOS:
        hf = project_health_factor(
            collateral_value_usd,
            debt_value_usd,
            liq_threshold_bps,
            collateral_price_change_pct=s.get("collateral_change_pct", 0.0),
            debt_price_change_pct=s.get("debt_change_pct", 0.0),
        )
        out.append({"scenario": s["name"], "health_factor": hf, "would_liquidate": hf < 1.0})
    return out
