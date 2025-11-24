import json
from pathlib import Path

import requests

from .config import get_chain_config, get_api_key


def _get_base_url_v2(chain: str) -> str:
    """
    Return the correct V2 base URL for each chain.

    We keep config.py as-is (V1 style), but here we explicitly
    route to the new /v2/api endpoints.
    """
    if chain == "ethereum":
        return "https://api.etherscan.io/v2/api"
    if chain == "bsc":
        return "https://api.bscscan.com/v2/api"
    if chain == "arbitrum":
        return "https://api.arbiscan.io/v2/api"
    if chain == "base":
        return "https://api.basescan.org/v2/api"

    # Fallback: use whatever is in config (not recommended for new chains)
    cfg = get_chain_config(chain)
    return cfg.explorer_base_url


def _call(chain: str, params: dict):
    """
    Call a *Scan explorer using the V2 API.

    - Uses /v2/api endpoints
    - Adds chainid parameter (required by V2)
    - Adds apikey from environment variable
    """
    cfg = get_chain_config(chain)
    base_url = _get_base_url_v2(chain)
    api_key = get_api_key(chain)

    full_params = dict(params)
    full_params["apikey"] = api_key
    # V2 requires chainid
    full_params["chainid"] = str(cfg.chain_id)

    resp = requests.get(base_url, params=full_params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status")
    if status == "0":
        # Explorer-specific error message
        raise RuntimeError(f"{chain} explorer error: {data}")

    return data.get("result")


def get_normal_transactions(chain: str, address: str):
    """
    Fetch 'normal' transactions for an address using V2
    Account -> Get Normal Transactions By Address.
    Docs: https://docs.etherscan.io/api-reference/endpoint/txlist
    """
    return _call(
        chain,
        {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 9999999999,
            "page": 1,
            "offset": 10000,  # up to 10k tx in one go
            "sort": "asc",
        },
    )


def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
