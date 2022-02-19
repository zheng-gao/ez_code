from typing import List


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
            weights = [None] * len(edges)
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
            if item is None and not self.is_weighted:
                item = self.mark
            return str(item) + (" " * (cell_size - len(str(item))))

        max_cell_size = 0
        for node_id in self.sorted_node_ids:
            max_cell_size = max(max_cell_size, len(str(node_id)))
        if self.is_weighted:
            for edges in self.nodes.values():
                for weight in edges.values():
                     max_cell_size = max(max_cell_size, len(str(weight)))
        max_cell_size += 1  # Add one space
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





graph = UndirectedGraph([[1,2],[2,3],[1,3]])
print(graph)