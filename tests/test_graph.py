from fixture.utils import check_list_copy, check_dict_copy
from ezcode.graph import NegativeCycleExist
from ezcode.graph.directed import DirectedGraph
from ezcode.graph.undirected import UndirectedGraph


def test_undirected_graph():
    graph_str = """
   A  B  C  D  E  
A     *  *        
B  *     *  *     
C  *  *     *  *  
D     *  *     *  
E        *  *     
"""[1:]
    graph = UndirectedGraph(edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]])
    benchmark = {
        "A": {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2},
        "B": {"A": 1, "B": 0, "C": 1, "D": 1, "E": 2},
        "C": {"A": 1, "B": 1, "C": 0, "D": 1, "E": 1},
        "D": {"A": 2, "B": 1, "C": 1, "D": 0, "E": 1},
        "E": {"A": 2, "B": 2, "C": 1, "D": 1, "E": 0}
    }
    assert graph_str == str(graph)
    for n1, b in benchmark.items():
        assert check_dict_copy(graph.bfs_path_value(n1), b)
        assert check_dict_copy(graph.dijkstra(n1), b)
        assert check_dict_copy(graph.spfa(n1), b)
        for n2 in benchmark.keys():
            assert benchmark[n1][n2] == graph.dfs_path_value(n1, n2)
    assert check_dict_copy(graph.floyd(), benchmark)


def test_undirected_weighted_graph():
    graph_str = """
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       
"""[1:]
    graph = UndirectedGraph(edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]], weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3])
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
        assert check_dict_copy(graph.dijkstra(n1), benchmark, resolution=resolution)
        assert check_dict_copy(graph.spfa(n1), benchmark, resolution=resolution)
        for n2 in benchmark_1.keys():
            assert abs(benchmark_1[n1][n2] - graph.dfs_path_value(n1, n2)) <= resolution
    assert check_dict_copy(graph.floyd(), benchmark_1)

    benchmark_2 = {
        "A": {"A": 1,      "B": 0.8,   "C": 0.648, "D": 0.72, "E": 0.5184},
        "B": {"A": 0.8,    "B": 1,     "C": 0.81,  "D": 0.9,  "E": 0.648 },
        "C": {"A": 0.648,  "B": 0.81,  "C": 1,     "D": 0.9,  "E": 0.8   },
        "D": {"A": 0.72,   "B": 0.9,   "C": 0.9,   "D": 1,    "E": 0.72  },
        "E": {"A": 0.5184, "B": 0.648, "C": 0.8,   "D": 0.72, "E": 1     }
    }
    for n1, benchmark in benchmark_2.items():
        assert check_dict_copy(graph.dijkstra(n1, self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark, resolution=resolution)
        assert check_dict_copy(graph.spfa(n1, self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark, resolution=resolution)
        for n2 in benchmark_2.keys():
            assert abs(benchmark_2[n1][n2] - graph.dfs_path_value(n1, n2, self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) <= resolution
    assert check_dict_copy(graph.floyd(self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2, resolution=resolution)


def test_negative_cycle_detection():
    graph = UndirectedGraph(edges=[["A","B"],["A","C"],["A","D"],["B","C"],["B","D"],["C","D"]], weights=[2, 3, 2, -3, 1, 1])
    try:
        graph.spfa("A", check_cycle=True)
    except NegativeCycleExist:
        assert True
    else:
        assert False


def test_directed_graph():
    graph_str = """
   a  b  c  d  e  f  
a           *        
b                 *  
c  *              *  
d     *              
e                    
f              *     
"""[1:]
    graph = DirectedGraph(edges=[("c","a"),("b","f"),("e",None),("a","d"),("c","f"),("d","b"),("f","e")])
    assert graph_str == str(graph)
    assert check_list_copy(graph.topological_order(), ["e", "f", "b", "d", "a", "c"])
    assert graph.is_acyclic_graph()
    assert not DirectedGraph(edges=[("a","b"),("b","a")]).is_acyclic_graph()
    graph_str = """
   a  b  c  d  e  f  
a     *              
b           *        
c  *  *           *  
d  *     *           
e                    
f           *        
"""[1:]
    graph = DirectedGraph(edges=[("a","b"),("c","b"),("d","a"),("b","d"),("c","a"),("d","c"),("c","f"),("f","d"),("e",None)])
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
        assert check_dict_copy(graph.bfs_path_value(n1), b)
        assert check_dict_copy(graph.dijkstra(n1), b)
        assert check_dict_copy(graph.spfa(n1), b)
        for n2 in benchmark.keys():
            assert benchmark[n1][n2] == graph.dfs_path_value(n1, n2)
    assert check_dict_copy(graph.floyd(), benchmark)


def test_directed_weighted_graph():
    pass







