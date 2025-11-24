from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import networkx as nx
import pandas as pd

@dataclass
class TxContractInfo:
    chain: str
    deployer: str
    contract_address: str
    tx_hash: str
    block_number: int

class MultichainGraphBuilder:
    def __init__(self):
        self.G = nx.DiGraph()

    def _norm(self, addr: str) -> str:
        return addr.lower()

    def add_deployments(self, items):
        for c in items:
            dep = self._norm(c.deployer)
            con = self._norm(c.contract_address)

            self.G.add_node(dep, type="deployer", chain=c.chain)
            self.G.add_node(con, type="contract", chain=c.chain)

            self.G.add_edge(
                dep,
                con,
                relation="DEPLOYED",
                chain=c.chain,
                tx_hash=c.tx_hash,
                block_number=c.block_number,
            )

    def compute_metrics(self):
        deg = dict(self.G.degree())
        nx.set_node_attributes(self.G, deg, "degree")
        nx.set_node_attributes(self.G, dict(self.G.in_degree()), "in_degree")
        nx.set_node_attributes(self.G, dict(self.G.out_degree()), "out_degree")

    def export(self, graph_path, nodes_path=None, edges_path=None):
        graph_path = Path(graph_path)
        graph_path.parent.mkdir(parents=True, exist_ok=True)
        nx.write_gexf(self.G, graph_path)

        if nodes_path:
            nodes_path = Path(nodes_path)
            nodes_path.parent.mkdir(parents=True, exist_ok=True)
            rows = []
            for n, a in self.G.nodes(data=True):
                r = {"id": n}
                r.update(a)
                rows.append(r)
            pd.DataFrame(rows).to_csv(nodes_path, index=False)

        if edges_path:
            edges_path = Path(edges_path)
            edges_path.parent.mkdir(parents=True, exist_ok=True)
            rows = []
            for u, v, a in self.G.edges(data=True):
                r = {"source": u, "target": v}
                r.update(a)
                rows.append(r)
            pd.DataFrame(rows).to_csv(edges_path, index=False)

def contracts_from_raw_json(chain: str, raw: List[Dict[str, Any]]) -> List[TxContractInfo]:
    items = []
    for tx in raw:
        addr = tx.get("contractAddress")
        if addr:
            items.append(
                TxContractInfo(
                    chain=chain,
                    deployer=tx.get("from"),
                    contract_address=addr,
                    tx_hash=tx.get("hash"),
                    block_number=int(tx.get("blockNumber", 0)),
                )
            )
    return items
