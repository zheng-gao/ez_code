from typing import List
from ezcode.array.heap import PriorityMap


class UndirectedGraph:
    def __init__(self, edges: List[list] = None, weights: list = None):
        self.nodes = dict()  # <node_id, <node_id, weight>>
        self.is_weighted: bool = weights is not None
        self.sorted_node_ids: list = None     # for print
        self.node_id_index_map: dict = None   # for print
        self.mark = "*"                       # for print
        if edges:
            self.build(edges=edges, weights=weights)

    def __len__(self):
        return len(self.nodes)

    def build(self, edges: List[list], weights: list = None):
        if weights is None:
            weights = [1] * len(edges)
        for (n1, n2), weight in zip(edges, weights):
            if n1 not in self.nodes:
                self.nodes[n1] = dict()
            if n2 not in self.nodes:
                self.nodes[n2] = dict()
            self.nodes[n1][n2] = self.nodes[n2][n1] = weight
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map = dict()
        for index, node_id in enumerate(self.sorted_node_ids):
            self.node_id_index_map[node_id] = index

    def __str__(self):
        def get_cell(cell_size, item=""):
            if item == 1 and not self.is_weighted:
                item = self.mark
            return str(item) + (" " * (cell_size - len(str(item))))

        max_cell_size = 0
        for node_id in self.sorted_node_ids:
            max_cell_size = max(max_cell_size, len(str(node_id)))
        if self.is_weighted:
            for edges in self.nodes.values():
                for weight in edges.values():
                     max_cell_size = max(max_cell_size, len(str(weight)))
        max_cell_size += 2  # Add two spaces in between
        output = get_cell(max_cell_size)
        for node_id in self.sorted_node_ids:
            output += get_cell(max_cell_size, node_id)
        output += "\n"
        for row in range(len(self)):
            n1 = self.sorted_node_ids[row]
            output += get_cell(max_cell_size, n1)
            for col in range(len(self)):
                n2 = self.sorted_node_ids[col]
                output += get_cell(max_cell_size, self.nodes[n1][n2]) if n2 in self.nodes[n1] else get_cell(max_cell_size)
            output += "\n"
        return output

    def print(self):
        print(self, end="")

    def dijkstra(self, src_node_id, dst_node_id, self_loop_value=0, path_value_init=float("inf"), path_value_func=lambda a, b: a + b, min_heap=True):
        path_values, visited, candidates = dict(), set(), PriorityMap({src_node_id:self_loop_value}, min_heap=min_heap)
        for node_id in self.nodes.keys():
            path_values[node_id] = self_loop_value if node_id == src_node_id else path_value_init
        while len(candidates) > 0:
            top_path_value, top_node_id = candidates.pop()
            visited.add(top_node_id)
            for node_id, weight in self.nodes[top_node_id].items():
                if node_id not in visited:
                    min_max_func = min if min_heap else max
                    path_values[node_id] = min_max_func(path_values[node_id], path_value_func(top_path_value, weight))
                    candidates.push(path_values[node_id], node_id)
        return path_values[dst_node_id]
