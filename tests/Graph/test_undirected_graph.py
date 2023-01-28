from ezcode.Utils import equal
from ezcode.Graph.GraphPathFinder import GraphPathFinder, NegativeCycleExistError, UnweightedGraphExpectedError
from ezcode.Graph.UndirectedGraph import UndirectedGraph


def test_undirected_graph_init():
    # weighted
    graphs = list()
    graphs.append(UndirectedGraph({("A", "B"): 1, ("A", "C"): 2, ("A", "D"): 3}))                  # dict<tuple(2), X>
    graphs.append(UndirectedGraph({("A", "B", 1), ("A", "C", 2), ("A", "D", 3)}))                  # set(tuple(3))
    graphs.append(UndirectedGraph([("A", "B", 1), ("A", "C", 2), ("A", "D", 3)]))                  # list(tuple(3))
    graphs.append(UndirectedGraph([["A", "B", 1], ["A", "C", 2], ["A", "D", 3]]))                  # list(list(3))
    graphs.append(UndirectedGraph(edges=[("A", "B"), ("A", "C"), ("A", "D")], weights=[1, 2, 3]))  # edges=list(list(2))
    graphs.append(UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]], weights=[1, 2, 3]))  # edges=list(tuple(2))
    graph_str = """
   A  B  C  D
A     1  2  3
B  1         
C  2         
D  3         
"""[1:]
    for g in graphs:
        assert str(g) == graph_str
    # unweighted
    graphs = list()
    graphs.append(UndirectedGraph({("A", "B"): None, ("A", "C"): None, ("A", "D"): None}))         # dict<tuple(2), None>
    graphs.append(UndirectedGraph({("A", "B", None), ("A", "C", None), ("A", "D", None)}))         # set(tuple(3))
    graphs.append(UndirectedGraph({("A", "B"), ("A", "C"), ("A", "D")}))                           # set(tuple(2))
    graphs.append(UndirectedGraph([("A", "B", None), ("A", "C", None), ("A", "D", None)]))         # list(tuple(3))
    graphs.append(UndirectedGraph([["A", "B", None], ["A", "C", None], ["A", "D", None]]))         # list(list(3))
    graphs.append(UndirectedGraph([("A", "B"), ("A", "C"), ("A", "D")]))                           # list(tuple(2))
    graphs.append(UndirectedGraph([["A", "B"], ["A", "C"], ["A", "D"]]))                           # list(list(2))
    graphs.append(UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]]))                     # edges=list(list(2))
    graphs.append(UndirectedGraph(edges=[("A", "B"), ("A", "C"), ("A", "D")]))                     # edges=list(tuple(2))
    graph_str = """
   A  B  C  D
A     *  *  *
B  *         
C  *         
D  *         
"""[1:]
    for g in graphs:
        assert str(g) == graph_str


def test_undirected_graph_eulerian_path():
    """
    A ────── C
    │       ╱│╲
    │      ╱ │ ╲
    │     ╱  │  ╲
    │    ╱   │   E
    │   ╱    │  ╱
    │  ╱     │ ╱
    │ ╱      │╱
    B ────── D
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]])
    assert graph.eulerian_path(start_node="A") is None
    assert graph.eulerian_path(start_node="E") is None
    assert graph.eulerian_path(start_node="D") == ["D", "B", "A", "C", "D", "E", "C", "B"]
    assert graph.eulerian_path() == ["B", "A", "C", "B", "D", "C", "E", "D"]
    """
    A ── B
    │ ╲
    │  ╲
    D   C
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]])
    assert graph.eulerian_path() is None


def test_undirected_unweighted_graph():
    """
    A ────── C
    │       ╱│╲
    │      ╱ │ ╲
    │     ╱  │  ╲
    │    ╱   │   E
    │   ╱    │  ╱
    │  ╱     │ ╱
    │ ╱      │╱
    B ────── D
    """
    graph_str = """
   A  B  C  D  E
A     *  *      
B  *     *  *   
C  *  *     *  *
D     *  *     *
E        *  *   
"""[1:]
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]])
    assert not graph.is_weighted
    assert graph_str == str(graph)
    path_finder = GraphPathFinder(graph=graph)
    benchmark = {
        "A": {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2},
        "B": {"A": 1, "B": 0, "C": 1, "D": 1, "E": 2},
        "C": {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1},
        "D": {"A": 2, "B": 1, "C": 1, "D": 0, "E": 1},
        "E": {"A": 2, "B": 2, "C": 1, "D": 1, "E": 0}
    }
    for n1, b in benchmark.items():
        assert path_finder.bfs(n1) == (None, b)
        assert path_finder.dijkstra(n1) == (None, b)
        assert path_finder.spfa(n1) == (None, b)
        for n2 in benchmark.keys():
            assert path_finder.backtracking(n1, n2)[0] == benchmark[n1][n2]
    assert path_finder.floyd() == benchmark
    assert path_finder.bfs("E", "A") == (2, ["E", "C", "A"])
    assert path_finder.dijkstra("E", "A") == (2, ["E", "C", "A"])
    assert path_finder.spfa("E", "A") == (2, ["E", "C", "A"])
    assert path_finder.backtracking("B", "E") == (2, [["B", "C", "E"], ["B", "D", "E"]])
    assert path_finder.bfs("B", "B") == (0, ["B"])
    assert path_finder.dijkstra("B", "B") == (0, ["B"])
    assert path_finder.spfa("B", "B") == (0, ["B"])
    assert path_finder.backtracking("B", "B") == (0, [["B"]])


def test_undirected_weighted_graph():
    """
    A ──0.2─ C 
    │       ╱│ ╲
    │      ╱ │ 0.8
   0.8    ╱  │   ╲
    │    ╱  0.9   E
    │  0.5   │   ╱
    │  ╱     │ 0.3
    │ ╱      │ ╱
    B ──0.9─ D
    """
    graph_str = """
     A    B    C    D    E
A       0.8  0.2          
B  0.8       0.5  0.9     
C  0.2  0.5       0.9  0.8
D       0.9  0.9       0.3
E            0.8  0.3     
"""[1:]
    graph = UndirectedGraph({
        ("A", "B"): 0.8,
        ("A", "C"): 0.2,
        ("B", "C"): 0.5,
        ("B", "D"): 0.9,
        ("C", "D"): 0.9,
        ("C", "E"): 0.8,
        ("D", "E"): 0.3
    })
    assert graph_str == str(graph)
    assert graph.is_weighted
    path_finder = GraphPathFinder(graph=graph)
    resolution = 0.0001
    benchmark_1 = {
        "A": {"A": 0,   "B": 0.7, "C": 0.2, "D": 1.1, "E": 1.0},
        "B": {"A": 0.7, "B": 0,   "C": 0.5, "D": 0.9, "E": 1.2},
        "C": {"A": 0.2, "B": 0.5, "C": 0,   "D": 0.9, "E": 0.8},
        "D": {"A": 1.1, "B": 0.9, "C": 0.9, "D": 0,   "E": 0.3},
        "E": {"A": 1.0, "B": 1.2, "C": 0.8, "D": 0.3, "E": 0  }
    }
    for n1, benchmark in benchmark_1.items():
        assert equal(path_finder.dijkstra(n1), (None, benchmark), resolution=resolution)
        assert equal(path_finder.spfa(n1), (None, benchmark), resolution=resolution)
        for n2 in benchmark_1.keys():
            assert equal(benchmark_1[n1][n2], path_finder.backtracking(n1, n2)[0], resolution=resolution)
    assert equal(path_finder.floyd(), benchmark_1)
    assert path_finder.dijkstra("B", "E") == (1.2, ["B", "D", "E"])
    assert path_finder.spfa("B", "E") == (1.2, ["B", "D", "E"])
    assert path_finder.backtracking("B", "E") == (1.2, [["B", "D", "E"]])

    benchmark_2 = {
        "A": {"A": 1,      "B": 0.8,   "C": 0.648, "D": 0.72, "E": 0.5184},
        "B": {"A": 0.8,    "B": 1,     "C": 0.81,  "D": 0.9,  "E": 0.648 },
        "C": {"A": 0.648,  "B": 0.81,  "C": 1,     "D": 0.9,  "E": 0.8   },
        "D": {"A": 0.72,   "B": 0.9,   "C": 0.9,   "D": 1,    "E": 0.72  },
        "E": {"A": 0.5184, "B": 0.648, "C": 0.8,   "D": 0.72, "E": 1     }
    }
    config = {"self_loop_weight": 1, "disconnected_edge_weight": 0, "path_value_func": (lambda a,b: a * b), "is_min": False}
    for n1, benchmark in benchmark_2.items():
        assert equal(path_finder.dijkstra(n1, **config), (None, benchmark), resolution=resolution)
        assert equal(path_finder.spfa(n1, **config), (None, benchmark), resolution=resolution)
        for n2 in benchmark_2.keys():
            assert equal(benchmark_2[n1][n2], path_finder.backtracking(n1, n2, **config)[0], resolution=resolution)
    assert equal(path_finder.floyd(**config), benchmark_2, resolution=resolution)
    assert equal(path_finder.dijkstra("B", "E", **config), (0.648, ["B", "D", "C", "E"]), resolution=resolution)
    assert equal(path_finder.spfa("B", "E", **config), (0.648, ["B", "D", "C", "E"]), resolution=resolution)
    assert equal(path_finder.backtracking("B", "E", **config), (0.648, [["B", "D", "C", "E"]]), resolution=resolution)
    try:
        path_finder.bfs("B", "E")
        assert False
    except UnweightedGraphExpectedError:
        assert True


def test_negative_cycle_detection():
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"], ["B", "C"], ["B", "D"], ["C", "D"]], weights=[2, 3, 2, -3, 1, 1])
    path_finder = GraphPathFinder(graph=graph)
    try:
        path_finder.spfa("A", check_cycle=True)
        assert False
    except NegativeCycleExistError:
        assert True


def test_is_connected():
    """
    A ────── C
    │       ╱│╲
    │      ╱ │ ╲
    │     ╱  │  ╲
    │    ╱   │   E
    │   ╱    │  ╱
    │  ╱     │ ╱
    │ ╱      │╱
    B ────── D
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]])
    assert graph.is_connected()
    """
    A ────── C
    │       ╱
    │      ╱
    │     ╱
    │    ╱       E
    │   ╱       ╱
    │  ╱       ╱
    │ ╱       ╱
    B        D
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["D", "E"]])
    assert not graph.is_connected()




