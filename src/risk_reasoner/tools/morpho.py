"""Fetch a Morpho Blue position summary.

Morpho Blue's contract emits Position events but the simplest way to read a
user's position is through the on-chain `position(marketId, user)` view.
"""
from web3 import Web3


MORPHO_BLUE = "0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb"

POSITION_ABI = [
    {
        "inputs": [
            {"name": "id", "type": "bytes32"},
            {"name": "user", "type": "address"},
        ],
        "name": "position",
        "outputs": [
            {"name": "supplyShares", "type": "uint256"},
            {"name": "borrowShares", "type": "uint128"},
            {"name": "collateral", "type": "uint128"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


def fetch_morpho_position(rpc_url: str, market_id: str, user: str):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(MORPHO_BLUE), abi=POSITION_ABI)
    supply, borrow, collateral = c.functions.position(
        Web3.to_bytes(hexstr=market_id), Web3.to_checksum_address(user),
    ).call()
    return {
        "user": user,
        "market_id": market_id,
        "supply_shares": int(supply),
        "borrow_shares": int(borrow),
        "collateral": int(collateral),
    }
