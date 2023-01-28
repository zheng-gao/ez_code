from collections.abc import MutableMapping, Sequence
from typing import Iterable, Callable


class Graph:
    def __init__(self, weight_to_str: Callable = lambda x: str(x)):
        self.nodes = dict()
        self.is_weighted: bool = False
        self.weight_to_str = weight_to_str  # for print only

    def __len__(self) -> int:
        return len(self.nodes)

    def __contains__(self, node) -> bool:
        return node in self.nodes

    def update(self,
        edges_and_weights: Iterable = None,                          # Data input option I (overrides others)
        edges: Iterable[Sequence] = None, weights: Iterable = None,  # Data input option II
    ):
        is_weighted = False
        if edges_and_weights:
            if isinstance(edges_and_weights, MutableMapping):
                for edge, weight in edges_and_weights.items():
                    if weight is None:
                        self.insert_edge(edge, 1)
                    else:
                        self.insert_edge(edge, weight)
                        is_weighted = True
            else:
                for item in edges_and_weights:
                    if len(item) == 2 or item[2] is None:
                        self.insert_edge(edge=(item[0], item[1]), weight=1)
                    else:
                        self.insert_edge(edge=(item[0], item[1]), weight=item[2])
                        is_weighted = True
        elif not weights:
            for edge in edges:
                self.insert_edge(edge, 1)
        else:
            if len(edges) != len(weights):
                raise ValueError("Unmatched edges and weights")
            for edge, weight in zip(edges, weights):
                self.insert_edge(edge, weight)
            is_weighted = True
        self.is_weighted = is_weighted

    def get_weight(self, node_1, node_2, is_outgoing: bool = True):
        edges = self.get_edges(node_1, is_outgoing)
        if edges is None:
            return None
        return edges[node_2] if node_2 in edges else None

    def get_edges(self, node_id, is_outgoing: bool = True):
        raise NotImplementedError

    def insert_edge(self, edge: Sequence, weight=None):
        raise NotImplementedError

    def remove_edge(self, edge: Sequence):
        raise NotImplementedError

    def get_all_edges(self):
        raise NotImplementedError

    def __str__(self):
        sorted_nodes = sorted(self.nodes.keys())
        first_column_size, cell_size, table = 0, 0, [["", *sorted_nodes]]
        for node_1 in sorted_nodes:
            cell_size = max(cell_size, len(str(node_1)))
            first_column_size = max(first_column_size, len(str(node_1)))
            table_row = [node_1]
            for node_2 in sorted_nodes:
                weight = self.get_weight(node_1, node_2)
                if weight is not None:
                    weight_str = self.weight_to_str(weight) if self.is_weighted else "*"
                    table_row.append(weight_str)
                    cell_size = max(cell_size, len(weight_str))
                else:
                    table_row.append("")
            table.append(table_row)
        string = ""
        for row in table:
            for index, col in enumerate(row):
                if index == 0:
                    string += col.rjust(first_column_size, " ")
                else:
                    string += col.rjust(cell_size, " ")
                if index < len(row) - 1:
                    string += "  "
            string += "\n"
        return string
        # return "\n".join("  ".join(map(lambda x: x.rjust(cell_size, " "), row)) for row in table)
        # return array_to_string(
        #     table, indent="", cell_size=cell_size + 1, alignment='r',
        #     with_bracket_and_comma=False, deepest_iterable_one_line=True
        # )

    def print(self):
        print(self, end="")

    def copy_nodes(self) -> dict:
        raise NotImplementedError

    def eulerian_path(self, start_node=None) -> list:
        """
            Eulerian path existence condition: Graph is connected
            For Undirected Graph:
                Either every vertex has even degree or excatly two vertices has odd degree
            For Directed Graph:
                At most one vertex has indegree-outdegree=1 and at most one vertex has outdegree-indegree=1
                Rest all vertices have equal outdegree and indegree

            https://en.wikipedia.org/wiki/Eulerian_path
            Hierholzer's algorithm
            Step 1:
                Undirected Graph: Find the node that has odd degree as the starting node
                Directed Graph: Find the node that has outdegree-indegree=1 as the starting node
            Step 2:
                If no such node exist, you can start from any node
            Step 3:
                Do DFS on start node and append to the path

            O(V+E)
        """
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError



