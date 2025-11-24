import pandas as pd

def load_nodes_edges(nodes_path, edges_path):
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)
    return nodes, edges

def build_deployer_features(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    d = nodes[nodes["type"]=="deployer"].copy().set_index("id")

    dep_edges = edges[edges["relation"]=="DEPLOYED"].copy()
    counts = dep_edges.groupby("source")["target"].nunique()
    d["n_contracts"] = counts.reindex(d.index).fillna(0).astype(int)

    if "out_degree" in d.columns:
        d["avg_out_degree"] = d["out_degree"].astype(float)
    else:
        d["avg_out_degree"] = 0.0

    d["n_chains"] = 1

    return d.reset_index().rename(columns={"id":"deployer"})
