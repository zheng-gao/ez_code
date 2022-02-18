from typing import List


class UndirectedGraph:
    def __init__(self, edges: List[list] = None, weights: list = None):
        self.nodes = dict()  # <node_id, <node_id, weight>>
        self.is_weighted = weights is not None
        if edges:
            self.build(edges=edges, weights=weights)

    def __len__(self):
        return len(self.nodes)

    def build(self, edges: List[list], weights: list = None):
        if weights is None:
            weights = [None] * len(edges)
        for (n1, n2), weight in zip(edges, weights):
            if n1 not in nodes:
                nodes[n1] = dict()
            if n2 not in nodes:
                nodes[n2] = dict()
            nodes[n1][n2] = nodes[n2][n1] = weight
