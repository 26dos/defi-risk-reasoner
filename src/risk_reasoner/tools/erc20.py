"""ERC20 helpers — balances, decimals, symbol lookup with caching."""
from functools import lru_cache

from web3 import Web3


ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
     "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals",
     "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol",
     "outputs": [{"name": "", "type": "string"}], "type": "function"},
]


@lru_cache(maxsize=512)
def token_metadata(rpc_url: str, token: str):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(token), abi=ERC20_ABI)
    try:
        decimals = int(c.functions.decimals().call())
    except Exception:
        decimals = 18
    try:
        symbol = c.functions.symbol().call()
    except Exception:
        symbol = "?"
    return {"decimals": decimals, "symbol": symbol}


def balance_of(rpc_url: str, token: str, holder: str) -> int:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    c = w3.eth.contract(address=Web3.to_checksum_address(token), abi=ERC20_ABI)
    return int(c.functions.balanceOf(Web3.to_checksum_address(holder)).call())
