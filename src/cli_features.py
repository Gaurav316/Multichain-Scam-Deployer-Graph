import argparse
from pathlib import Path
import pandas as pd
from .features import load_nodes_edges, build_deployer_features
from .risk_rules import score_deployer_row

def main():
    parser = argparse.ArgumentParser(description="Build deployer features.")
    parser.add_argument("--nodes", required=True)
    parser.add_argument("--edges", required=True)
    parser.add_argument("--out", required=True)
    a = parser.parse_args()

    nodes, edges = load_nodes_edges(a.nodes, a.edges)
    df = build_deployer_features(nodes, edges)
    risks = df.apply(score_deployer_row, axis=1, result_type="expand")
    final = pd.concat([df, risks], axis=1)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(out, index=False)
    print(f"[✓] Saved {out}")

if __name__ == "__main__":
    main()
