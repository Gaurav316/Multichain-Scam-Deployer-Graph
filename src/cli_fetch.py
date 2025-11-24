import argparse
from pathlib import Path
from .explorers import get_normal_transactions, save_json

def main():
    parser = argparse.ArgumentParser(description="Fetch deployer tx history.")
    parser.add_argument("--chain", required=True)
    parser.add_argument("--deployer", required=True)
    parser.add_argument("--out", required=True)
    a = parser.parse_args()

    txs = get_normal_transactions(a.chain, a.deployer)
    save_json({"chain": a.chain, "deployer": a.deployer, "txs": txs}, Path(a.out))
    print(f"[✓] Saved {len(txs)} txs")

if __name__ == "__main__":
    main()
