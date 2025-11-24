import argparse
from pathlib import Path
from .explorers import load_json
from .graph_builder import MultichainGraphBuilder, contracts_from_raw_json

def main():
    parser = argparse.ArgumentParser(description="Build deployer graph.")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--out_graph", required=True)
    parser.add_argument("--out_nodes")
    parser.add_argument("--out_edges")
    a = parser.parse_args()

    builder = MultichainGraphBuilder()

    for p in a.inputs:
        obj = load_json(Path(p))
        chain = obj["chain"]
        txs = obj["txs"]
        contracts = contracts_from_raw_json(chain, txs)
        builder.add_deployments(contracts)
        print(f"[+] {p}: {len(contracts)} deployments")

    builder.compute_metrics()
    builder.export(a.out_graph, a.out_nodes, a.out_edges)
    print("[✓] Graph exported.")

if __name__ == "__main__":
    main()
