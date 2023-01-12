from ezcode.Graph import Graph


class UndirectedGraph(Graph):
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
        # self.nodes = {node_id, {node_id, weight}}
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
            for next_node_id in self.get_edges(node_id).keys():
                if next_node_id not in visited_edges:
                    visited_edges[next_node_id] = set()
                if next_node_id not in visited_edges[node_id] and node_id not in visited_edges[next_node_id]:
                    visited_edges[node_id].add(next_node_id)
                    visited_edges[next_node_id].add(node_id)
                    _dfs(next_node_id)
            eulerian_path_nodes.append(node_id)

        _dfs(node_id=start_node_id)
        return eulerian_path_nodes[::-1]


