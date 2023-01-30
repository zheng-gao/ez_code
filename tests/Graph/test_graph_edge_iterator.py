from ezcode.Graph.DirectedGraph import DirectedGraph
from ezcode.Graph.UndirectedGraph import UndirectedGraph
from ezcode.Graph.GraphEdgeIterator import GraphEdgeIterator


def test_iterator_on_undirected_graph():
    def _test(benchmark):
        for edge in UndirectedGraph(benchmark):
            if edge in benchmark:
                benchmark.remove(edge)
            else:
                if len(edge) == 2:
                    reversed_edge = (edge[1], edge[0])
                else:
                    reversed_edge = (edge[1], edge[0], edge[2])
                benchmark.remove(reversed_edge)
        assert len(benchmark) == 0

    _test(set([("A", "B", 1), ("A", "C", 2), ("A", "D", 3)]))
    _test(set([("A", "B"), ("A", "C"), ("B", "C"), ("D", "E")]))
    _test(set([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E")]))
    _test(set([("A", "B", 1), ("B", "C", 2), ("C", "D", 3), ("E", "F", 4), ("F", "G", 5), ("G", "E", 6)]))
    _test(set([("A", "B"), ("B", "C"), ("C", "D"), ("E", "F"), ("F", "G"), ("B", "E"), ("G", "D")]))
    _test(set([("A", "B"), ("B", "C"), ("C", "D"), ("E", "F"), ("F", "G"), ("B", "F"), ("G", "D")]))


def test_iterator_on_directed_graph():
    def _test(benchmark):
        for edge in DirectedGraph(benchmark):
            if edge in benchmark:
                benchmark.remove(edge)
        assert len(benchmark) == 0

    _test(set([("A", "B", 1), ("A", "C", 2), ("A", "D", 3), ("B", "A", 0)]))
    _test(set([("A", "B"), ("A", "C"), ("C", "B"), ("E", "D"), ("B", "C"), ("D", "E")]))
    _test(set([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "E"), ("C", "B")]))
    _test(set([("A", "B", 1), ("B", "C", 2), ("C", "D", 3), ("E", "F", 4), ("F", "G", 5), ("G", "E", 6), ("F", "E", 2)]))
    _test(set([("A", "B"), ("B", "C"), ("C", "D"), ("E", "F"), ("F", "G"), ("B", "E"), ("G", "D"), ("B", "A"), ("E", "B")]))
    _test(set([("A", "B"), ("B", "C"), ("C", "D"), ("E", "F"), ("F", "G"), ("B", "F"), ("G", "D"), ("D", "C"), ("G", "F")]))

