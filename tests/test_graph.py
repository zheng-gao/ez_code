from fixture.utils import equal_list, equal_dict
from ezcode.graph import NegativeCycleExist
from ezcode.graph.directed import DirectedGraph
from ezcode.graph.undirected import UndirectedGraph


def test_undirected_graph():
    """
    A ------ C
    |       /|\
    |      / | \
    |     /  |  \
    |    /   |   E
    |   /    |  /
    |  /     | /
    | /      |/
    B ------ D
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
    benchmark = {
        "A": {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2},
        "B": {"A": 1, "B": 0, "C": 1, "D": 1, "E": 2},
        "C": {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1},
        "D": {"A": 2, "B": 1, "C": 1, "D": 0, "E": 1},
        "E": {"A": 2, "B": 2, "C": 1, "D": 1, "E": 0}
    }
    assert graph_str == str(graph)
    for n1, b in benchmark.items():
        assert equal_dict(graph.bfs_path_value(n1), b)
        assert equal_dict(graph.dijkstra(n1), b)
        assert equal_dict(graph.spfa(n1), b)
        for n2 in benchmark.keys():
            assert equal_list(benchmark[n1][n2], graph.dfs_path_value(n1, n2))
    assert equal_dict(graph.floyd(), benchmark)


def test_undirected_weighted_graph():
    """
    A --0.2- C 
    |       /| \
    |      / | 0.8
   0.8    /  |   \
    |    /  0.9   E
    |  0.5   |   /
    |  /     | 0.3
    | /      | /
    B --0.9- D
    """
    graph_str = """
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       
"""[1:]
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]], weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3])
    assert graph_str == str(graph)
    resolution = 0.0001
    benchmark_1 = {
        "A": {"A": 0,   "B": 0.7, "C": 0.2, "D": 1.1, "E": 1.0},
        "B": {"A": 0.7, "B": 0,   "C": 0.5, "D": 0.9, "E": 1.2},
        "C": {"A": 0.2, "B": 0.5, "C": 0,   "D": 0.9, "E": 0.8},
        "D": {"A": 1.1, "B": 0.9, "C": 0.9, "D": 0,   "E": 0.3},
        "E": {"A": 1.0, "B": 1.2, "C": 0.8, "D": 0.3, "E": 0  }
    }
    for n1, benchmark in benchmark_1.items():
        assert equal_dict(graph.dijkstra(n1), benchmark, resolution=resolution)
        assert equal_dict(graph.spfa(n1), benchmark, resolution=resolution)
        for n2 in benchmark_1.keys():
            assert equal_list(benchmark_1[n1][n2], graph.dfs_path_value(n1, n2), resolution=resolution)
    assert equal_dict(graph.floyd(), benchmark_1)

    benchmark_2 = {
        "A": {"A": 1,      "B": 0.8,   "C": 0.648, "D": 0.72, "E": 0.5184},
        "B": {"A": 0.8,    "B": 1,     "C": 0.81,  "D": 0.9,  "E": 0.648 },
        "C": {"A": 0.648,  "B": 0.81,  "C": 1,     "D": 0.9,  "E": 0.8   },
        "D": {"A": 0.72,   "B": 0.9,   "C": 0.9,   "D": 1,    "E": 0.72  },
        "E": {"A": 0.5184, "B": 0.648, "C": 0.8,   "D": 0.72, "E": 1     }
    }
    for n1, benchmark in benchmark_2.items():
        assert equal_dict(graph.dijkstra(n1, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a * b, min_max_func=max), benchmark, resolution=resolution)
        assert equal_dict(graph.spfa(n1, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), benchmark, resolution=resolution)
        for n2 in benchmark_2.keys():
            assert equal_list(benchmark_2[n1][n2], graph.dfs_path_value(n1, n2, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), resolution=resolution)
    assert equal_dict(graph.floyd(self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), benchmark_2, resolution=resolution)


def test_negative_cycle_detection():
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"], ["B", "C"], ["B", "D"], ["C", "D"]], weights=[2, 3, 2, -3, 1, 1])
    try:
        graph.spfa("A", check_cycle=True)
    except NegativeCycleExist:
        assert True
    else:
        assert False


def test_directed_graph():
    """
    a <----- c 
    |        |
    |        v
    |        f ---> e
    |        ^
    v        |
    d -----> b
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
    assert equal_list(graph.topological_order(), ["e", "f", "b", "d", "a", "c"])
    assert graph.is_acyclic_graph()
    assert not DirectedGraph(edges=[("a", "b"), ("b", "a")]).is_acyclic_graph()
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
        assert equal_dict(graph.bfs_path_value(n1), b)
        assert equal_dict(graph.dijkstra(n1), b)
        assert equal_dict(graph.spfa(n1), b)
        for n2 in benchmark.keys():
            assert equal_list(benchmark[n1][n2], graph.dfs_path_value(n1, n2))
    assert equal_dict(graph.floyd(), benchmark)


def test_directed_weighted_graph():
    graph_str = """
      a     b     c     d     e     f     
a           0.8                           
b                       0.8               
c     0.5   0.7                     0.6   
d     0.6         0.8                     
e                                         
f                       0.4               
"""[1:]
    graph = DirectedGraph(
        edges=[("a", "b"), ("c", "b"), ("d", "a"), ("b", "d"), ("c", "a"), ("d", "c"), ("c", "f"), ("f", "d"), ("e", None)],
        weights=[0.8, 0.7, 0.6, 0.8, 0.5, 0.8, 0.6, 0.4, None]
    )
    assert graph_str == str(graph)
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
        assert equal_dict(graph.dijkstra(n1), benchmark, resolution=resolution)
        assert equal_dict(graph.spfa(n1), benchmark, resolution=resolution)
        for n2 in benchmark_1.keys():
            assert equal_list(benchmark_1[n1][n2], graph.dfs_path_value(n1, n2), resolution=resolution)
    assert equal_dict(graph.floyd(), benchmark_1, resolution=resolution)

    benchmark_2 = {
        "a": {"a": 1,    "b": 0.8,   "c": 0.512, "d": 0.64, "e": 0, "f": 0.3072},
        "b": {"a": 0.48, "b": 1,     "c": 0.64,  "d": 0.8,  "e": 0, "f": 0.384 },
        "c": {"a": 0.5,  "b": 0.7,   "c": 1,     "d": 0.56, "e": 0, "f": 0.6   },
        "d": {"a": 0.6,  "b": 0.56,  "c": 0.8,   "d": 1,    "e": 0, "f": 0.48  },
        "e": {"a": 0,    "b": 0,     "c": 0,     "d": 0,    "e": 1, "f": 0     },
        "f": {"a": 0.24, "b": 0.224, "c": 0.32,  "d": 0.4,  "e": 0, "f": 1     }
    }
    for n1, benchmark in benchmark_2.items():
        assert equal_dict(graph.dijkstra(n1, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), benchmark, resolution=resolution)
        assert equal_dict(graph.spfa(n1, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), benchmark, resolution=resolution)
        for n2 in benchmark_2.keys():
            assert equal_list(benchmark_2[n1][n2], graph.dfs_path_value(n1, n2, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), resolution=resolution)
    assert equal_dict(graph.floyd(self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a, b: a * b, min_max_func=max), benchmark_2, resolution=resolution)


def test_eulerian_path():
    """
    A ------ C
    |       /|\
    |      / | \
    |     /  |  \
    |    /   |   E
    |   /    |  /
    |  /     | /
    | /      |/
    B ------ D
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]])
    assert graph.eulerian_path(start_node="A") is None
    assert graph.eulerian_path(start_node="E") is None
    assert graph.eulerian_path(start_node="D") == ["D", "B", "A", "C", "D", "E", "C", "B"]
    assert graph.eulerian_path() == ["B", "A", "C", "B", "D", "C", "E", "D"]
    """
    A -- B
    | \
    |  \
    D   C
    """
    graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]])
    assert graph.eulerian_path() is None
    """
    A <--- B 
    |      ^
    |      |
    v      |
    D ---> C <--- E
           |
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
    A <--- B ---> F
    |      ^
    |      |
    v      |
    D ---> C <--- E
    """
    graph = DirectedGraph(edges=[["B", "A"], ["A", "D"], ["D", "C"], ["C", "B"], ["E", "C"], ["B", "F"]])
    assert graph.eulerian_path() is None 




