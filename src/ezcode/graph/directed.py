from collections import deque
from typing import List
from ezcode.graph import Graph


class DirectedGraph(Graph):
    def __init__(self, edges: List[list] = None, weights: list = None, mark: str = "*"):
        super().__init__(is_weighted=(weights is not None), mark=mark)
        # self.nodes = {node_id: {"i": {node_id: weight}, "o": {node_id: weight}}
        if edges:
            self.build(edges=edges, weights=weights)

    def build(self, edges: List[list], weights: list = None):
        if weights is None:
            weights = [1] * len(edges)
        for (i, o), weight in zip(edges, weights):
            if i is not None and o is not None:
                if i not in self.nodes:
                    self.nodes[i] = {"i": dict(), "o": dict()}
                if o not in self.nodes:
                    self.nodes[o] = {"i": dict(), "o": dict()}
                self.nodes[i]["o"][o] = self.nodes[o]["i"][i] = weight
            elif i is not None:
                if i not in self.nodes:
                    self.nodes[i] = {"i": dict(), "o": dict()}
            elif o is not None:
                if o not in self.nodes:
                    self.nodes[o] = {"i": dict(), "o": dict()}
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map = dict()
        for index, node_id in enumerate(self.sorted_node_ids):
            self.node_id_index_map[node_id] = index
            self.cell_size = max(self.cell_size, len(str(node_id)))
        for weight in weights:
            self.cell_size = max(self.cell_size, len(str(weight)))
        self.cell_size += 2  # Add two spaces in between

    def get_weight(self, incoming, outgoing):
        return self.nodes[incoming]["o"][outgoing] if outgoing in self.nodes[incoming]["o"] else None

    def copy_nodes(self):
        new_nodes = dict()
        for node_id, edges in self.nodes.items():
            new_nodes[node_id] = {"i": dict(), "o": dict()}
            for incoming, weight in edges["i"].items():
                new_nodes[node_id]["i"][incoming] = weight
            for outgoing, weight in edges["o"].items():
                new_nodes[node_id]["o"][outgoing] = weight
        return new_nodes

    def topological_order(self):
        topological_order = list()
        no_outgoing_nodes = deque()
        nodes = self.copy_nodes()
        for node_id, edges in nodes.items():
            if len(edges["o"]) == 0:
                no_outgoing_nodes.append(node_id)
        while len(no_outgoing_nodes) > 0:
            node_id = no_outgoing_nodes.popleft()
            topological_order.append(node_id)
            for incoming in nodes[node_id]["i"].keys():
                del nodes[incoming]["o"][node_id]
                if len(nodes[incoming]["o"]) == 0:
                    no_outgoing_nodes.append(incoming)
        return topological_order

    def is_acyclic_graph(self):
        return len(self.topological_order()) == len(self)


            


