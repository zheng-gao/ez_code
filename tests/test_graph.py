from ezcode.array.utils import is_copied
from fixture.graph import dag, dag_string, non_dag
from ezcode.graph.undirected import UndirectedGraph


def test_graph_string():
    assert str(dag) == dag_string


def test_topological_order():
    assert is_copied(dag.topological_order(), ["e", "f", "b", "d", "a", "c"])


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
    graph = UndirectedGraph(
        edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]])
    assert graph_str == str(graph)
    assert 2 == graph.dfs_path_value("A", "E")
    assert 2 == graph.dfs_path_value("E", "B")
    assert 2 == graph.dijkstra("A", "E")
    assert 2 == graph.dijkstra("E", "B")

def test_undirected_weighted_graph():
    graph_str = """
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       
"""[1:]
    graph = UndirectedGraph(
        edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]],
        weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3])
    assert graph_str == str(graph)
    resolution = 0.0001
    assert abs(1.0 - graph.dfs_path_value("A", "E")) < resolution
    assert abs(1.1 - graph.dfs_path_value("A", "D")) < resolution
    assert abs(1.2 - graph.dfs_path_value("E", "B")) < resolution
    assert abs(0.5184 - graph.dfs_path_value("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(0.72 - graph.dfs_path_value("A", "D", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(0.648 - graph.dfs_path_value("E", "B", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(1.0 - graph.dijkstra("A", "E")) < resolution
    assert abs(1.1 - graph.dijkstra("A", "D")) < resolution
    assert abs(1.2 - graph.dijkstra("E", "B")) < resolution
    assert abs(0.5184 - graph.dijkstra("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(0.72 - graph.dijkstra("A", "D", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
    assert abs(0.648 - graph.dijkstra("E", "B", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)) < resolution
