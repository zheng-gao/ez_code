class Graph:
    def __init__(self, is_weighted: bool, mark: str = "*"):
        self.nodes = dict()
        self.is_weighted: bool = is_weighted
        self.sorted_node_ids: list = None     # for print
        self.node_id_index_map: dict = None   # for print
        self.mark = mark                      # for print
        self.cell_size = 1                    # for print

    def __len__(self) -> int:
        return len(self.nodes)

    def build_graph(self, edge_weight_dict: dict = None, edges: list[list] = None, weights: list = None):
        pass

    def _cell(self, item=None) -> str:
        if not self.is_weighted and item == 1:
            item = self.mark
        if item is None:
            item = ""
        return str(item) + (" " * (self.cell_size - len(str(item))))

    def get_weight(self, node_id_1, node_id_2, is_outgoing: bool = True):
        edges = self.get_edges(node_id_1, is_outgoing)
        return edges[node_id_2] if node_id_2 in edges else None

    def get_edges(self, node_id, is_outgoing: bool = True):
        raise NotImplementedError

    def __str__(self):
        output = self._cell()
        for node_id in self.sorted_node_ids:
            output += self._cell(node_id)
        output += "\n"
        for row in range(len(self)):
            incoming = self.sorted_node_ids[row]
            output += self._cell(incoming)
            for col in range(len(self)):
                outgoing = self.sorted_node_ids[col]
                output += self._cell(self.get_weight(incoming, outgoing))
            output += "\n"
        return output

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
        pass



