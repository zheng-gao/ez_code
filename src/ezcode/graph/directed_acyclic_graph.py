from collections import deque
from typing import List


class ActivityOnVertexGraph:
    class Node():
        def __init__(self, node_id=None, from_nodes=None, to_nodes=None):
            self.node_id = node_id
            self.from_nodes = from_nodes  # set(Node)
            self.to_nodes = to_nodes      # set(Node)

    def __init__(self, from_to_list=None):
        self.nodes = None  # dict(node_id, Node)
        self.sorted_node_ids = None       # for print
        self.node_id_index_map = None     # for print
        if from_to_list:
            self.build(from_to_list=from_to_list)

    def size(self):
        return len(self.nodes)

    def build(self, from_to_list: List[list]):
        if not self.nodes:
            self.nodes = dict()
        for from_to_pair in from_to_list:
            from_id, to_id = from_to_pair
            if from_id:
                if from_id not in self.nodes:
                    self.nodes[from_id] = self.Node(node_id=from_id)
                from_node = self.nodes[from_id]
            else:
                from_node = None
            if to_id:
                if to_id not in self.nodes:
                    self.nodes[to_id] = self.Node(node_id=to_id)
                to_node = self.nodes[to_id]
            else:
                to_node = None
            if from_node and to_node:
                if not from_node.to_nodes:
                    from_node.to_nodes = set()
                from_node.to_nodes.add(to_node)
                if not to_node.from_nodes:
                    to_node.from_nodes = set()
                to_node.from_nodes.add(from_node)
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map, index = dict(), 0
        for node_id in self.sorted_node_ids:
            self.node_id_index_map[node_id] = index
            index += 1

    def __str__(self, column_size=2, mark="*"):
        def get_cell(column_size, item=""):
            return str(item) + " " * (column_size - len(str(item)))
        matrix = self.generate_matrix()
        for node_id in self.sorted_node_ids:
            if len(node_id) + 1 > column_size:
                column_size = len(node_id) + 1
        output = get_cell(column_size)
        for node_id in self.sorted_node_ids:
            output += get_cell(column_size, node_id)
        output += "\n"
        for row in range(self.size()):
            node_id = self.sorted_node_ids[row]
            output += get_cell(column_size, node_id)
            for col in range(self.size()):
                output += get_cell(column_size, mark) if matrix[row][col] else get_cell(column_size)
            output += "\n"
        return output

    def print(self):
        print(self, end="")

    def generate_matrix(self):
        matrix = [[False] * self.size() for _ in range(self.size())]
        for node_id in self.sorted_node_ids:
            node = self.nodes[node_id]
            if node.to_nodes:
                for to_node in node.to_nodes:
                    from_index = self.node_id_index_map[node.node_id]
                    to_index = self.node_id_index_map[to_node.node_id]
                    matrix[from_index][to_index] = True
        return matrix

    def copy_nodes(self):
        new_nodes = dict()
        for node_id, node in self.nodes.items():
            if node.from_nodes:
                new_from_nodes = set()
                for from_node in node.from_nodes:
                    if from_node.node_id not in new_nodes:
                        new_nodes[from_node.node_id] = self.Node(node_id=from_node.node_id)
                    new_from_nodes.add(new_nodes[from_node.node_id])
            else:
                new_from_nodes = None
            if node.to_nodes:
                new_to_nodes = set()
                for to_node in node.to_nodes:
                    if to_node.node_id not in new_nodes:
                        new_nodes[to_node.node_id] = self.Node(node_id=to_node.node_id)
                    new_to_nodes.add(new_nodes[to_node.node_id])
            else:
                new_to_nodes = None
            if node_id not in new_nodes:
                new_nodes[node_id] = self.Node(node_id, new_from_nodes, new_to_nodes)
            else:
                new_nodes[node_id].from_nodes = new_from_nodes
                new_nodes[node_id].to_nodes = new_to_nodes
        return new_nodes

    def topological_order(self):
        topological_order = list()
        nodes_without_to = deque()
        for _, node in self.copy_nodes().items():
            if not node.to_nodes or len(node.to_nodes) == 0:
                nodes_without_to.append(node)
        while len(nodes_without_to) > 0:
            node = nodes_without_to.pop()
            topological_order.append(node.node_id)
            if node.from_nodes:
                for from_node in node.from_nodes:
                    from_node.to_nodes.remove(node)
                    if not from_node.to_nodes:
                        nodes_without_to.append(from_node)
        return topological_order

    def is_directed_acyclic_graph(self):
        return len(self.topological_order()) == self.size()


            


