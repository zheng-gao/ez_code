from collections import deque
from typing import List


class DirectedGraph:
    class Node():
        def __init__(self, node_id=None, src_nodes: set = None, dst_nodes: set = None):
            self.node_id = node_id
            self.src_nodes = src_nodes  # set(Node)
            self.dst_nodes = dst_nodes  # set(Node)

    def __init__(self, edges: List[list] = None):
        self.nodes = None  # dict(node_id, Node)
        self.sorted_node_ids = None     # for print
        self.node_id_index_map = None   # for print
        if edges:
            self.build(edges=edges)

    def __len__(self):
        return len(self.nodes)

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
        for row in range(len(self)):
            node_id = self.sorted_node_ids[row]
            output += get_cell(column_size, node_id)
            for col in range(len(self)):
                output += get_cell(column_size, mark) if matrix[row][col] else get_cell(column_size)
            output += "\n"
        return output

    def build(self, edges: List[list]):
        if not self.nodes:
            self.nodes = dict()
        for (src_id, dst_id) in edges:
            if src_id:
                if src_id not in self.nodes:
                    self.nodes[src_id] = self.Node(node_id=src_id)
                src_node = self.nodes[src_id]
            else:
                src_node = None
            if dst_id:
                if dst_id not in self.nodes:
                    self.nodes[dst_id] = self.Node(node_id=dst_id)
                dst_node = self.nodes[dst_id]
            else:
                dst_node = None
            if src_node and dst_node:
                if not src_node.dst_nodes:
                    src_node.dst_nodes = set()
                src_node.dst_nodes.add(dst_node)
                if not dst_node.src_nodes:
                    dst_node.src_nodes = set()
                dst_node.src_nodes.add(src_node)
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map, index = dict(), 0
        for node_id in self.sorted_node_ids:
            self.node_id_index_map[node_id] = index
            index += 1

    def print(self):
        print(self, end="")

    def generate_matrix(self):
        matrix = [[False] * len(self) for _ in range(len(self))]
        for node_id in self.sorted_node_ids:
            node = self.nodes[node_id]
            if node.dst_nodes:
                for dst_node in node.dst_nodes:
                    src_index = self.node_id_index_map[node.node_id]
                    dst_index = self.node_id_index_map[dst_node.node_id]
                    matrix[src_index][dst_index] = True
        return matrix

    def copy_nodes(self):
        new_nodes = dict()
        for node_id, node in self.nodes.items():
            if node.src_nodes:
                new_src_nodes = set()
                for src_node in node.src_nodes:
                    if src_node.node_id not in new_nodes:
                        new_nodes[src_node.node_id] = self.Node(node_id=src_node.node_id)
                    new_src_nodes.add(new_nodes[src_node.node_id])
            else:
                new_src_nodes = None
            if node.dst_nodes:
                new_dst_nodes = set()
                for dst_node in node.dst_nodes:
                    if dst_node.node_id not in new_nodes:
                        new_nodes[dst_node.node_id] = self.Node(node_id=dst_node.node_id)
                    new_dst_nodes.add(new_nodes[dst_node.node_id])
            else:
                new_dst_nodes = None
            if node_id not in new_nodes:
                new_nodes[node_id] = self.Node(node_id, new_src_nodes, new_dst_nodes)
            else:
                new_nodes[node_id].src_nodes = new_src_nodes
                new_nodes[node_id].dst_nodes = new_dst_nodes
        return new_nodes

    def topological_order(self):
        topological_order = list()
        nodes_without_dst = deque()
        for _, node in self.copy_nodes().items():
            if not node.dst_nodes or len(node.dst_nodes) == 0:
                nodes_without_dst.append(node)
        while len(nodes_without_dst) > 0:
            node = nodes_without_dst.pop()
            topological_order.append(node.node_id)
            if node.src_nodes:
                for src_node in node.src_nodes:
                    src_node.dst_nodes.remove(node)
                    if not src_node.dst_nodes:
                        nodes_without_dst.append(src_node)
        return topological_order

    def is_directed_acyclic_graph(self):
        return len(self.topological_order()) == len(self)


            


