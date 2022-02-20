# Directed Acyclic Graph

## Topological Sort

```
>>> from ezcode.graph.directed import DirectedGraph
>>> dependencies = [("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")]
>>> aov_graph = DirectedGraph(dependencies)
>>> aov_graph.print()
  a b c d e f 
a       *     
b           * 
c *         * 
d   *         
e             
f         *   
>>> print(aov_graph.topological_order())
['e', 'f', 'b', 'd', 'a', 'c']
>>> aov_graph.is_directed_acyclic_graph()
True
>>> circular_dependencies = [("a", "b"), ("b", "a")]
>>> DirectedGraph(circular_dependencies).is_directed_acyclic_graph()
False
```

# Undirected Graph

## Shortest Path Algorithm

```
>>> from ezcode.graph.undirected import UndirectedGraph
>>> graph = UndirectedGraph(
...     edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]],
...     weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3]
... )
>>> print(graph)
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       

>>> graph.dfs_path_value("A", "E")
1.0
>>> graph.dijkstra("A", "E")
1.0
>>> graph.spfa("A", "E")
1.0
>>> graph.dfs_path_value("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)
0.5184000000000001
>>> graph.dijkstra("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)
0.5184000000000001
>>> graph.spfa("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_max_func=max)
0.5184000000000001
```

## Detect Negative Cycle

```
>>> from ezcode.graph.undirected import UndirectedGraph
>>> graph = UndirectedGraph(
...     edges=[["A","B"],["A","C"],["A","D"],["B","C"],["B","D"],["C","D"]],
...     weights=[2, 3, 2, -3, 1, 1]
... )
>>> print(graph)
    A   B   C   D   
A       2   3   2   
B   2       -3  1   
C   3   -3      1   
D   2   1   1    

>>> graph.spfa("A", "B", check_negative_weight=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zgao/Desktop/study/ez_code/src/ezcode/graph/undirected.py", line 114, in spfa
    raise NegativeCycleExist()
ezcode.graph.NegativeCycleExist
```