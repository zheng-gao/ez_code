class GraphEdgeIterator:
    def __init__(self, graph):
        self.graph = graph
        self.node_iterator = iter(graph.nodes)
        self.edge_iterator = None
        self.from_node = None
        self.edges = None

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.edges is None:
                self.from_node = next(self.node_iterator)
                self.edges = self.graph.get_edges(self.from_node, is_outgoing=True)
                self.edge_iterator = iter(self.edges)
            try:
                to_node = next(self.edge_iterator)
                if self.graph.is_weighted:
                    return self.from_node, to_node, self.edges[to_node]
                else:
                    return self.from_node, to_node
            except StopIteration:
                self.edges = None


class UndirectedGraphEdgeIterator(GraphEdgeIterator):
    def __init__(self, graph):
        super().__init__(graph)
        self.visited = set()

    def __next__(self):
        while True:
            if self.edges is None:
                self.from_node = next(self.node_iterator)
                self.visited.add(self.from_node)
                self.edges = self.graph.get_edges(self.from_node, is_outgoing=True)
                self.edge_iterator = iter(self.edges)
            try:
                to_node = next(self.edge_iterator)
                while to_node in self.visited:
                    to_node = next(self.edge_iterator)
                if self.graph.is_weighted:
                    return self.from_node, to_node, self.edges[to_node]
                else:
                    return self.from_node, to_node
            except StopIteration:
                self.edges = None
