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

## Dijkstra Algorithm

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

>>> graph.dijkstra("A", "E")
1.0
>>> graph.dijkstra("A", "E", self_loop_value=1, path_value_init=0, path_value_func=lambda a,b: a*b, min_heap=False)
0.5184000000000001
```