import os
from dataclasses import dataclass

@dataclass
class ChainConfig:
    name: str
    explorer_base_url: str
    api_key_env: str
    chain_id: int

CHAIN_CONFIGS = {
    "ethereum": ChainConfig(
        name="ethereum",
        explorer_base_url="https://api.etherscan.io/v2/api",
        api_key_env="ETHERSCAN_API_KEY",
        chain_id=1,
    ),
    "bsc": ChainConfig(
        name="bsc",
        explorer_base_url="https://api.bscscan.com/v2/api",
        api_key_env="BSCSCAN_API_KEY",
        chain_id=56,
    ),
    "arbitrum": ChainConfig(
        name="arbitrum",
        explorer_base_url="https://api.arbiscan.io/v2/api",
        api_key_env="ARBISCAN_API_KEY",
        chain_id=42161,
    ),
    "base": ChainConfig(
        name="base",
        explorer_base_url="https://api.basescan.org/v2/api",
        api_key_env="BASESCAN_API_KEY",
        chain_id=8453,
    ),
}

def get_chain_config(chain: str) -> ChainConfig:
    if chain not in CHAIN_CONFIGS:
        raise ValueError(f"Unknown chain '{chain}'. Valid: {list(CHAIN_CONFIGS)}")
    return CHAIN_CONFIGS[chain]

def get_api_key(chain: str) -> str:
    cfg = get_chain_config(chain)
    key = os.getenv(cfg.api_key_env)
    if not key:
        raise RuntimeError(f"Missing API key env var: {cfg.api_key_env}")
    return key
