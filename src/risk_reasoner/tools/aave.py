"""Fetch an Aave V3 position summary for a wallet.

Aave V3 exposes a UiPoolDataProvider contract that returns all the data we
need in one call. We also normalize amounts into human-readable units.
"""
from web3 import Web3


# Aave V3 mainnet
POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fa4E2"
UI_DATA_PROVIDER = "0x91c0eA31b49B69Ea18607702c5d9aC360bf3dE7d"

USER_RESERVES_ABI = [
    {
        "inputs": [
            {"name": "provider", "type": "address"},
            {"name": "user", "type": "address"},
        ],
        "name": "getUserReservesData",
        "outputs": [
            {
                "components": [
                    {"name": "underlyingAsset", "type": "address"},
                    {"name": "scaledATokenBalance", "type": "uint256"},
                    {"name": "usageAsCollateralEnabledOnUser", "type": "bool"},
                    {"name": "stableBorrowRate", "type": "uint256"},
                    {"name": "scaledVariableDebt", "type": "uint256"},
                    {"name": "principalStableDebt", "type": "uint256"},
                    {"name": "stableBorrowLastUpdateTimestamp", "type": "uint256"},
                ],
                "name": "userReserves",
                "type": "tuple[]",
            },
            {"name": "userEMode", "type": "uint8"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


def fetch_aave_v3_position(rpc_url: str, addresses_provider: str, user: str):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(UI_DATA_PROVIDER), abi=USER_RESERVES_ABI)
    reserves, e_mode = c.functions.getUserReservesData(
        Web3.to_checksum_address(addresses_provider),
        Web3.to_checksum_address(user),
    ).call()
    return {
        "user": user,
        "e_mode": int(e_mode),
        "reserves": [
            {
                "asset": r[0],
                "atoken_scaled": int(r[1]),
                "as_collateral": bool(r[2]),
                "variable_debt_scaled": int(r[4]),
            }
            for r in reserves
        ],
    }
