from collections import deque
from ezcode.Graph import Graph


class DirectedGraph(Graph):
    def __init__(self, edge_weight_dict: dict = None, edges: list[list] = None, weights: list = None, mark: str = "*"):
        if edge_weight_dict is None:
            is_weighted = weights is not None
        else:
            is_weighted = False
            for weight in edge_weight_dict.values():
                if weight is not None:
                    is_weighted = True
                    break
        super().__init__(is_weighted=is_weighted, mark=mark)
        # self.nodes = {node_id: {"i": {node_id: weight}, "o": {node_id: weight}}
        if edge_weight_dict or edges:
            self.build_graph(edge_weight_dict=edge_weight_dict, edges=edges, weights=weights)

    def build_graph(self, edge_weight_dict: dict = None, edges: list[list] = None, weights: list = None):
        if edge_weight_dict:
            edges, weights = list(), list()
            for edge, weight in edge_weight_dict.items():
                edges.append(edge)
                if weight is not None:
                    weights.append(weight)
        if not weights:
            weights = [1] * len(edges)
        for (i, o), weight in zip(edges, weights):
            if i is not None and i not in self.nodes:
                self.nodes[i] = {"i": dict(), "o": dict()}
            if o is not None and o not in self.nodes:
                self.nodes[o] = {"i": dict(), "o": dict()}
            if i is not None and o is not None:
                self.nodes[i]["o"][o] = self.nodes[o]["i"][i] = weight
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
        return self.nodes[node_id]["o"] if is_outgoing else self.nodes[node_id]["i"]

    def copy_nodes(self) -> dict:
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

    def is_acyclic(self) -> bool:
        return len(self.topological_order()) == len(self)

    def eulerian_path(self, start_node=None) -> list:
        """
            Eulerian path existence condition on Directed Graph:
            Graph is connected
            At most 1 vertex has indegree-outdegree=1 (end) and at most 1 vertex has outdegree-indegree=1 (start)
            Rest all vertices have equal outdegree and indegree

            https://en.wikipedia.org/wiki/Eulerian_path
            Hierholzer's algorithm
            Step 1: Find the node that has outdegree-indegree=1 as the starting node
            Step 2: If no such node exist, you can start from any node
            Step 3: Do DFS on start node and append the node with no outgoing edges to the path
            Step 4: Reverse the path

            O(V+E)
        """
        if start_node is not None and start_node not in self.nodes:
            raise ValueError(f"Node {start_node} not found in graph")
        degree_delta_positive_one, degree_delta_negative_one, start_node_id = False, False, None
        for node_id in self.nodes:
            degree_delta = len(self.get_edges(node_id, is_outgoing=True)) - len(self.get_edges(node_id, is_outgoing=False))
            if degree_delta == 1:
                if degree_delta_positive_one:
                    return None
                else:
                    start_node_id = node_id
                    degree_delta_positive_one = True
                    if start_node is not None and start_node != node_id:
                        return None
            elif degree_delta == -1:
                if degree_delta_negative_one:
                    return None
                else:
                    degree_delta_negative_one = True
                    if start_node is not None and start_node == node_id:
                        return None
            elif degree_delta != 0:
                return None
            elif start_node_id is None:
                start_node_id = node_id
        if start_node is not None:
            start_node_id == start_node
        eulerian_path_nodes, visited_edges = list(), dict()

        def _dfs(node_id):
            if node_id not in visited_edges:
                visited_edges[node_id] = set()
            for outgoing_node_id in self.get_edges(node_id, is_outgoing=True).keys():
                if outgoing_node_id not in visited_edges[node_id]:
                    visited_edges[node_id].add(outgoing_node_id)
                    _dfs(outgoing_node_id)
            eulerian_path_nodes.append(node_id)

        _dfs(node_id=start_node_id)
        return eulerian_path_nodes[::-1]

    """
    Maximum Flow Algorithm

    Ford Fulkerson: O(F * |E|) where F is the maximum flow and the E is the number of edges
    1. Find an augmenting path
    2. Remove the flow value of the augmenting path from graph, adding inverse edges
    """
    # def ford_fulkerson(self, src_node_id, dst_node_id):
    #     nodes = self.copy_nodes()
    #     def dfs_find_augmenting_path(node_id, flow, visited_nodes: set):
    #         if node_id = dst_node_id:
    #             return flow
    #         for outgoing_node_id, weight in nodes[node_id]["o"].items():
    #             if outgoing_node_id not in visited_nodes:
    #                 visited_nodes.add(outgoing_node_id)
    #                 if weight > 0:
    #                     flow = dfs_find_augmenting_path(outgoing_node_id, min(flow, weight), visited_nodes)
    #                     if flow > 0:
    #                         nodes[node_id]["o"][outgoing_node_id] = weight - flow
    #                         # inverse edges: nodes[]
    #                         return flow
    #                 visited_nodes.remove(outgoing_node_id)
    #         return 0





