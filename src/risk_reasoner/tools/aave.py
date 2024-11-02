"""Fetch an Aave V3 position summary for a wallet."""
from web3 import Web3


POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fa4E2"

POOL_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"name": "totalCollateralBase", "type": "uint256"},
            {"name": "totalDebtBase", "type": "uint256"},
            {"name": "availableBorrowsBase", "type": "uint256"},
            {"name": "currentLiquidationThreshold", "type": "uint256"},
            {"name": "ltv", "type": "uint256"},
            {"name": "healthFactor", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


def fetch_aave_v3_summary(rpc_url: str, user: str):
    """Return liquidation-relevant aggregate state for a user.

    All amounts in Aave 'base units' (USD with 8 decimals on mainnet).
    healthFactor is in 1e18 units; >= 1e18 means safe.
    """
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(POOL), abi=POOL_ABI)
    r = c.functions.getUserAccountData(Web3.to_checksum_address(user)).call()
    total_collateral, total_debt, available_borrows, liq_threshold, ltv, hf = r
    return {
        "user": user,
        "total_collateral_usd": total_collateral / 1e8,
        "total_debt_usd": total_debt / 1e8,
        "available_borrows_usd": available_borrows / 1e8,
        "current_ltv_bps": int(ltv),
        "liquidation_threshold_bps": int(liq_threshold),
        "health_factor": hf / 1e18 if hf < (2**127) else float("inf"),
    }
