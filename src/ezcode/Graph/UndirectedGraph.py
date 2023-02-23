from collections.abc import Sequence
from collections import deque
from typing import Iterable, Callable

from ezcode.Graph.Graph import Graph
from ezcode.Graph.GraphEdgeIterator import UndirectedGraphEdgeIterator


class UndirectedGraph(Graph):
    def __init__(self,
        edges_and_weights: Iterable = None,                          # Data init option I (overrides others)
        edges: Sequence[Sequence] = None, weights: Sequence = None,  # Data init option II
        weight_to_str: Callable = lambda x: str(x)
    ):
        super().__init__(weight_to_str=weight_to_str)  # self.nodes = {node_id_1: {node_id_2: weight}}
        self.update(edges_and_weights, edges, weights)

    def __iter__(self):
        return UndirectedGraphEdgeIterator(self)

    def insert_edge(self, edge: Sequence, weight=None):
        n1, n2 = edge
        if n1 is not None and n1 not in self.nodes:
            self.nodes[n1] = dict()
        if n2 is not None and n2 not in self.nodes:
            self.nodes[n2] = dict()
        if n1 is not None and n2 is not None:
            self.nodes[n1][n2] = self.nodes[n2][n1] = weight

    def remove_edge(self, edge: Sequence):
        n1, n2 = edge
        del self.nodes[n1][n2]
        del self.nodes[n2][n1]

    def get_edges(self, node_id, is_outgoing: bool = True):
        if node_id not in self.nodes:
            return None
        return self.nodes[node_id]

    def get_all_edges(self):
        raise NotImplementedError

    def copy_nodes(self) -> dict:
        new_nodes = dict()
        for node_id, edges in self.nodes.items():
            new_nodes[node_id] = dict()
            for next_node_id, weight in edges.items():
                new_nodes[node_id][next_node_id] = weight
        return new_nodes

    def eulerian_path(self, start_node=None):
        """
            Eulerian path existence condition on Undirected Graph:
            Graph is connected
            Either every vertex has even degree or excatly two vertices has odd degree

            https://en.wikipedia.org/wiki/Eulerian_path
            Hierholzer's algorithm
            Step 1: Find the node that has odd degree
            Step 2: If no such node exist, you can start from any node
            Step 3: Do DFS on start node and append the node with no edges to the path
            Step 4: Reverse the path

            O(V+E)
        """
        if start_node is not None and start_node not in self.nodes:
            raise ValueError(f"Node {start_node} not found in graph")
        odd_degree_nodes, start_node_id = list(), None
        for node_id in self.nodes:
            if len(self.get_edges(node_id)) % 2 == 1:
                odd_degree_nodes.append(node_id)
                if len(odd_degree_nodes) > 2:
                    return None
            elif start_node_id is None:
                start_node_id = node_id
        if len(odd_degree_nodes) == 0:
            if start_node is not None:
                start_node_id = start_node
        elif len(odd_degree_nodes) == 2:
            if start_node is None:
                start_node_id = odd_degree_nodes[0]
            else:
                if start_node not in odd_degree_nodes:
                    return None
                start_node_id = start_node
        else:
            return None
        eulerian_path_nodes, visited_edges = list(), dict()

        def _dfs(node_id):
            if node_id not in visited_edges:
                visited_edges[node_id] = set()
            for next_node_id in self.get_edges(node_id):
                if next_node_id not in visited_edges:
                    visited_edges[next_node_id] = set()
                if next_node_id not in visited_edges[node_id] and node_id not in visited_edges[next_node_id]:
                    visited_edges[node_id].add(next_node_id)
                    visited_edges[next_node_id].add(node_id)
                    _dfs(next_node_id)
            eulerian_path_nodes.append(node_id)

        _dfs(node_id=start_node_id)
        return eulerian_path_nodes[::-1]

    def is_connected(self) -> bool:
        if len(self) == 0:
            return False
        visited, queue = set(), deque([self.get_a_node()])
        while len(queue) > 0:
            node_id = queue.popleft()
            visited.add(node_id)
            for neighbor_id in self.get_edges(node_id):
                if neighbor_id not in visited:
                    queue.append(neighbor_id)
        return len(self) == len(visited)

    def is_connected_with(self, other) -> bool:
        raise NotImplementedError("TBD")

    def is_bipartite(self) -> bool:
        """
        nodes can be partitioned into two independent sets A and B
        every edge connects a node in set A and a node in set B
        """
        set_a, set_b, visited, unvisited, queue = set(), set(), set(), set(self.nodes), deque()
        while len(unvisited) > 0:  # for disconnected sub-graphs
            node = next(iter(unvisited))
            set_a.add(node)
            queue.append(node)
            while len(queue) > 0:
                node = queue.popleft()
                visited.add(node)
                unvisited.discard(node)
                for neighbor in self.get_edges(node):
                    if neighbor not in visited:
                        if node in set_a:
                            if neighbor in set_a:
                                return False
                            set_b.add(neighbor)
                        else:
                            if neighbor in set_b:
                                return False
                            set_a.add(neighbor)
                        queue.append(neighbor)
        return True









