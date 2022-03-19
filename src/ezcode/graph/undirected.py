from ezcode.graph import Graph
from typing import List


class UndirectedGraph(Graph):
    def __init__(self, edges: List[list] = None, weights: list = None, mark: str = "*"):
        super().__init__(is_weighted=(weights is not None), mark=mark)
        # self.nodes = {node_id, {node_id, weight}}
        if edges:
            self.build(edges=edges, weights=weights)

    def build(self, edges: List[list], weights: list = None):
        if weights is None:
            weights = [1] * len(edges)
        for (n1, n2), weight in zip(edges, weights):
            if n1 is not None and n1 not in self.nodes:
                self.nodes[n1] = dict()
            if n2 is not None and n2 not in self.nodes:
                self.nodes[n2] = dict()
            if n1 is not None and n2 is not None:
                self.nodes[n1][n2] = self.nodes[n2][n1] = weight
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map = dict()
        for index, node_id in enumerate(self.sorted_node_ids):
            self.node_id_index_map[node_id] = index
            self.cell_size = max(self.cell_size, len(str(node_id)))
        for weight in weights:
            self.cell_size = max(self.cell_size, len(str(weight)))
        self.cell_size += 2  # Add two spaces in between

    def get_edges(self, node_id, is_outgoing: bool = True):
        return self.nodes[node_id]
