"""Project a position's health factor under hypothetical price moves."""


def project_health_factor(
    collateral_value_usd: float,
    debt_value_usd: float,
    liquidation_threshold_bps: int,
    collateral_price_change_pct: float = 0.0,
    debt_price_change_pct: float = 0.0,
) -> float:
    """Compute health factor under price move.

    HF = (collateral_value * liq_threshold) / debt_value

    A move of -X% on collateral price scales collateral_value by (1 - X/100).
    A move of +X% on debt price scales debt_value by (1 + X/100).
    """
    new_collateral = collateral_value_usd * (1 + collateral_price_change_pct / 100)
    new_debt = debt_value_usd * (1 + debt_price_change_pct / 100)
    if new_debt <= 0:
        return float("inf")
    return new_collateral * (liquidation_threshold_bps / 10_000) / new_debt


def liquidation_distance(
    collateral_value_usd: float,
    debt_value_usd: float,
    liquidation_threshold_bps: int,
) -> float:
    """Return the % drop in collateral price that would put HF at exactly 1.0.

    Positive number means 'collateral can drop this much before liquidation'.
    """
    if debt_value_usd <= 0:
        return float("inf")
    needed = debt_value_usd / (liquidation_threshold_bps / 10_000)
    if needed >= collateral_value_usd:
        return 0.0
    return (1 - needed / collateral_value_usd) * 100
