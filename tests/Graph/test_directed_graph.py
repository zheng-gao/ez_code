from ezcode.Utils import equal
from ezcode.Graph.GraphPathFinder import GraphPathFinder, UnweightedGraphExpectedError
from ezcode.Graph.DirectedGraph import DirectedGraph


def test_directed_graph_init():
    # weighted
    graphs = list()
    graphs.append(DirectedGraph({("A", "B"): 1, ("A", "C"): 2, ("A", "D"): 3}))                  # dict<tuple(2), X>
    graphs.append(DirectedGraph({("A", "B", 1), ("A", "C", 2), ("A", "D", 3)}))                  # set(tuple(3))
    graphs.append(DirectedGraph([("A", "B", 1), ("A", "C", 2), ("A", "D", 3)]))                  # list(tuple(3))
    graphs.append(DirectedGraph([["A", "B", 1], ["A", "C", 2], ["A", "D", 3]]))                  # list(list(3))
    graphs.append(DirectedGraph(edges=[("A", "B"), ("A", "C"), ("A", "D")], weights=[1, 2, 3]))  # edges=list(list(2))
    graphs.append(DirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]], weights=[1, 2, 3]))  # edges=list(tuple(2))
    graph_str = """
   A  B  C  D
A     1  2  3
B            
C            
D            
"""[1:]
    for g in graphs:
        assert str(g) == graph_str
        assert g.is_weighted
    # unweighted
    graphs = list()
    graphs.append(DirectedGraph({("A", "B"): None, ("A", "C"): None, ("A", "D"): None}))         # dict<tuple(2), None>
    graphs.append(DirectedGraph({("A", "B", None), ("A", "C", None), ("A", "D", None)}))         # set(tuple(3))
    graphs.append(DirectedGraph({("A", "B"), ("A", "C"), ("A", "D")}))                           # set(tuple(2))
    graphs.append(DirectedGraph([("A", "B", None), ("A", "C", None), ("A", "D", None)]))         # list(tuple(3))
    graphs.append(DirectedGraph([["A", "B", None], ["A", "C", None], ["A", "D", None]]))         # list(list(3))
    graphs.append(DirectedGraph([("A", "B"), ("A", "C"), ("A", "D")]))                           # list(tuple(2))
    graphs.append(DirectedGraph([["A", "B"], ["A", "C"], ["A", "D"]]))                           # list(list(2))
    graphs.append(DirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]]))                     # edges=list(list(2))
    graphs.append(DirectedGraph(edges=[("A", "B"), ("A", "C"), ("A", "D")]))                     # edges=list(tuple(2))
    graph_str = """
   A  B  C  D
A     *  *  *
B            
C            
D            
"""[1:]
    for g in graphs:
        assert str(g) == graph_str
        assert not g.is_weighted


def test_directed_graph_eulerian_path():
    """
    A <─── B 
    │      ^
    │      │
    v      │
    D ───> C <─── E
           │
           v
           F
    """
    graph = DirectedGraph(edges=[["B", "A"], ["A", "D"], ["D", "C"], ["C", "B"], ["E", "C"], ["C", "F"]])
    assert graph.eulerian_path(start_node="A") is None
    assert graph.eulerian_path(start_node="B") is None
    assert graph.eulerian_path(start_node="C") is None
    assert graph.eulerian_path(start_node="D") is None
    assert graph.eulerian_path(start_node="F") is None
    assert graph.eulerian_path(start_node="E") == ["E", "C", "B", "A", "D", "C", "F"]
    assert graph.eulerian_path(start_node="E") == graph.eulerian_path()
    """
    A <─── B ───> F
    │      ^
    │      │
    v      │
    D ───> C <─── E
    """
    graph = DirectedGraph(edges=[["B", "A"], ["A", "D"], ["D", "C"], ["C", "B"], ["E", "C"], ["B", "F"]])
    assert graph.eulerian_path() is None 


def test_directed_unweighted_graph():
    """
    a <───── c 
    │        │
    │        v
    │        f ───> e
    │        ^
    v        │
    d ─────> b
    """
    graph_str = """
   a  b  c  d  e  f
a           *      
b                 *
c  *              *
d     *            
e                  
f              *   
"""[1:]
    graph = DirectedGraph(edges=[("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")])
    assert graph_str == str(graph)
    assert graph.topological_order() == ["e", "f", "b", "d", "a", "c"]
    assert graph.is_acyclic()
    assert not DirectedGraph(edges=[("a", "b"), ("b", "a")]).is_acyclic()
    """
    ┌──────> c     e
    │       ╱│╲
    │      ╱ │ ╲
    │     ╱  │  ╲
    │    ╱   │   ╲
    │   v    v    v
    │  f     a ──> b
    │   ╲    ^    ╱
    │    ╲   │   ╱
    │     ╲  │  ╱
    │      ╲ │ ╱
    │       v│v
    └─────── d
    """
    graph_str = """
   a  b  c  d  e  f
a     *            
b           *      
c  *  *           *
d  *     *         
e                  
f           *      
"""[1:]
    graph = DirectedGraph(edges=[("a", "b"), ("c", "b"), ("d", "a"), ("b", "d"), ("c", "a"), ("d", "c"), ("c", "f"), ("f", "d"), ("e", None)])
    assert graph_str == str(graph)
    assert not graph.is_weighted
    path_finder = GraphPathFinder(graph=graph)
    x = float("inf")
    benchmark = {
        "a": {"a": 0, "b": 1, "c": 3, "d": 2, "e": x, "f": 4},
        "b": {"a": 2, "b": 0, "c": 2, "d": 1, "e": x, "f": 3},
        "c": {"a": 1, "b": 1, "c": 0, "d": 2, "e": x, "f": 1},
        "d": {"a": 1, "b": 2, "c": 1, "d": 0, "e": x, "f": 2},
        "e": {"a": x, "b": x, "c": x, "d": x, "e": 0, "f": x},
        "f": {"a": 2, "b": 3, "c": 2, "d": 1, "e": x, "f": 0}
    }
    assert graph_str == str(graph)
    for n1, b in benchmark.items():
        assert path_finder.bfs(n1) == (None, b)
        assert path_finder.dijkstra(n1) == (None, b)
        assert path_finder.spfa(n1) == (None, b)
        for n2 in benchmark.keys():
            assert benchmark[n1][n2] == path_finder.backtracking(n1, n2)[0]
    assert path_finder.floyd() == benchmark
    assert path_finder.bfs("f", "a") == (2, ["f", "d", "a"])
    assert path_finder.dijkstra("f", "a") == (2, ["f", "d", "a"])
    assert path_finder.spfa("f", "a") == (2, ["f", "d", "a"])
    assert path_finder.backtracking("f", "a") == (2, [["f", "d", "a"]])


def test_directed_weighted_graph():
    """
    ┌──────> c     e
    │       ╱│╲
    │    0.6 │ 0.7
    │     ╱ 0.5 ╲
    │    ╱   │   ╲
    │   v    v .8 v
    │  f     a ──> b
    │   ╲    ^    ╱
    │   0.4  │  0.8
   0.8    ╲ 0.6 ╱
    │      ╲ │ ╱
    │       v│v
    └─────── d
    """
    graph_str = """
     a    b    c    d    e    f
a       0.8                    
b                 0.8          
c  0.5  0.7                 0.6
d  0.6       0.8               
e                              
f                 0.4          
"""[1:]
    graph = DirectedGraph(
        edges=[("a", "b"), ("c", "b"), ("d", "a"), ("b", "d"), ("c", "a"), ("d", "c"), ("c", "f"), ("f", "d"), ("e", None)],
        weights=[0.8, 0.7, 0.6, 0.8, 0.5, 0.8, 0.6, 0.4, None]
    )
    assert graph_str == str(graph)
    assert graph.is_weighted
    path_finder = GraphPathFinder(graph=graph)
    x, resolution = float("inf"), 0.0001
    benchmark_1 = {
        "a": {"a": 0,   "b": 0.8, "c": 2.4, "d": 1.6, "e": x, "f": 3.0, },
        "b": {"a": 1.4, "b": 0,   "c": 1.6, "d": 0.8, "e": x, "f": 2.2, },
        "c": {"a": 0.5, "b": 0.7, "c": 0,   "d": 1.0, "e": x, "f": 0.6, },
        "d": {"a": 0.6, "b": 1.4, "c": 0.8, "d": 0,   "e": x, "f": 1.4, },
        "e": {"a": x,   "b": x,   "c": x,   "d": x,   "e": 0, "f": x,   },
        "f": {"a": 1.0, "b": 1.8, "c": 1.2, "d": 0.4, "e": x, "f": 0,   }
    }
    for n1, benchmark in benchmark_1.items():
        assert equal(path_finder.dijkstra(n1), (None, benchmark), resolution=resolution)
        assert equal(path_finder.spfa(n1), (None, benchmark), resolution=resolution)
        for n2 in benchmark_1.keys():
            assert equal(benchmark_1[n1][n2], path_finder.backtracking(n1, n2)[0], resolution=resolution)
    assert equal(path_finder.floyd(), benchmark_1, resolution=resolution)
    assert path_finder.dijkstra("f", "b") == (1.8, ["f", "d", "a", "b"])
    assert path_finder.spfa("f", "b") == (1.8, ["f", "d", "a", "b"])
    assert path_finder.backtracking("f", "b") == (1.8, [["f", "d", "a", "b"]])
    try:
        path_finder.bfs("f", "b")
        assert False
    except UnweightedGraphExpectedError:
        assert True

    benchmark_2 = {
        "a": {"a": 1,    "b": 0.8,   "c": 0.512, "d": 0.64, "e": 0, "f": 0.3072},
        "b": {"a": 0.48, "b": 1,     "c": 0.64,  "d": 0.8,  "e": 0, "f": 0.384 },
        "c": {"a": 0.5,  "b": 0.7,   "c": 1,     "d": 0.56, "e": 0, "f": 0.6   },
        "d": {"a": 0.6,  "b": 0.56,  "c": 0.8,   "d": 1,    "e": 0, "f": 0.48  },
        "e": {"a": 0,    "b": 0,     "c": 0,     "d": 0,    "e": 1, "f": 0     },
        "f": {"a": 0.24, "b": 0.224, "c": 0.32,  "d": 0.4,  "e": 0, "f": 1     }
    }
    config = {"self_loop_weight": 1, "disconnected_edge_weight": 0, "path_value_func": (lambda a,b: a * b), "is_min": False}
    for n1, benchmark in benchmark_2.items():
        assert equal(path_finder.dijkstra(n1, **config), (None, benchmark), resolution=resolution)
        assert equal(path_finder.spfa(n1, **config), (None, benchmark), resolution=resolution)
        for n2 in benchmark_2.keys():
            assert equal(benchmark_2[n1][n2], path_finder.backtracking(n1, n2, **config)[0], resolution=resolution)
    assert equal(path_finder.floyd(**config), benchmark_2, resolution=resolution)
    assert equal(path_finder.dijkstra("f", "b", **config), (0.224, ["f", "d", "c", "b"]), resolution=resolution)
    assert equal(path_finder.spfa("f", "b", **config), (0.224, ["f", "d", "c", "b"]), resolution=resolution)
    assert equal(path_finder.backtracking("f", "b", **config), (0.224, [["f", "d", "c", "b"]]), resolution=resolution)



