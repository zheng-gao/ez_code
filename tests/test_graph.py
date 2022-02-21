from fixture.graph import dag, dag_string, non_dag
from fixture.utils import check_list_copy, check_dict_copy
from ezcode.graph import NegativeCycleExist
from ezcode.graph.undirected import UndirectedGraph


def test_graph_string():
    assert str(dag) == dag_string


def test_topological_order():
    assert check_list_copy(dag.topological_order(), ["e", "f", "b", "d", "a", "c"])


def test_is_directed_acyclic_graph():
    assert dag.is_directed_acyclic_graph()
    assert not non_dag.is_directed_acyclic_graph()


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
    assert benchmark["A"]["E"] == graph.dfs_path_value("A", "E")
    assert benchmark["E"]["B"] == graph.dfs_path_value("E", "B")
    assert check_dict_copy(graph.bfs_path_value("A"), benchmark["A"])
    assert check_dict_copy(graph.bfs_path_value("E"), benchmark["E"])
    assert check_dict_copy(graph.dijkstra("A"), benchmark["A"])
    assert check_dict_copy(graph.dijkstra("E"), benchmark["E"])
    assert check_dict_copy(graph.spfa("A"), benchmark["A"])
    assert check_dict_copy(graph.spfa("E"), benchmark["E"])
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
    benchmark_1 = {
        "A": {"A": 0,   "B": 0.7, "C": 0.2, "D": 1.1, "E": 1.0},
        "B": {"A": 0.7, "B": 0,   "C": 0.5, "D": 0.9, "E": 1.2},
        "C": {"A": 0.2, "B": 0.5, "C": 0,   "D": 0.9, "E": 0.8},
        "D": {"A": 1.1, "B": 0.9, "C": 0.9, "D": 0,   "E": 0.3},
        "E": {"A": 1.0, "B": 1.2, "C": 0.8, "D": 0.3, "E": 0  }
    }
    benchmark_2 = {
        "A": {"A": 1,      "B": 0.8,   "C": 0.648, "D": 0.72, "E": 0.5184},
        "B": {"A": 0.8,    "B": 1,     "C": 0.81,  "D": 0.9,  "E": 0.648 },
        "C": {"A": 0.648,  "B": 0.81,  "C": 1,     "D": 0.9,  "E": 0.8   },
        "D": {"A": 0.72,   "B": 0.9,   "C": 0.9,   "D": 1,    "E": 0.72  },
        "E": {"A": 0.5184, "B": 0.648, "C": 0.8,   "D": 0.72, "E": 1     }
    }
    resolution = 0.0001
    assert graph_str == str(graph)
    assert abs(benchmark_1["A"]["E"] - graph.dfs_path_value("A", "E")) < resolution
    assert abs(benchmark_1["A"]["D"] - graph.dfs_path_value("A", "D")) < resolution
    assert abs(benchmark_1["E"]["B"] - graph.dfs_path_value("E", "B")) < resolution
    assert abs(benchmark_2["A"]["E"] - graph.dfs_path_value("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(benchmark_2["A"]["D"] - graph.dfs_path_value("A", "D", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(benchmark_2["E"]["B"] - graph.dfs_path_value("E", "B", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert check_dict_copy(graph.dijkstra("A"), benchmark_1["A"], resolution=resolution)
    assert check_dict_copy(graph.dijkstra("E"), benchmark_1["E"], resolution=resolution)
    assert check_dict_copy(graph.dijkstra("A", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2["A"], resolution=resolution)
    assert check_dict_copy(graph.dijkstra("E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2["E"], resolution=resolution)
    assert check_dict_copy(graph.spfa("A"), benchmark_1["A"], resolution=resolution)
    assert check_dict_copy(graph.spfa("E"), benchmark_1["E"], resolution=resolution)
    assert check_dict_copy(graph.spfa("A", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2["A"], resolution=resolution)
    assert check_dict_copy(graph.spfa("E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2["E"], resolution=resolution)
    assert check_dict_copy(graph.floyd(), benchmark_1, resolution=resolution)
    assert check_dict_copy(graph.floyd(self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max), benchmark_2, resolution=resolution)

def test_negative_cycle_detection():
    graph = UndirectedGraph(edges=[["A","B"],["A","C"],["A","D"],["B","C"],["B","D"],["C","D"]], weights=[2, 3, 2, -3, 1, 1])
    try:
        graph.spfa("A", check_cycle=True)
    except NegativeCycleExist:
        assert True
    else:
        assert False





