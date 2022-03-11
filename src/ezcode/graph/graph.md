# Directed Graph

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
>>> aov_graph.is_acyclic_graph()
True
>>> circular_dependencies = [("a", "b"), ("b", "a")]
>>> DirectedGraph(circular_dependencies).is_acyclic_graph()
False
```

## Shortest Path Algorithm

### Unweighted
```
>>> from ezcode.graph.directed import DirectedGraph
>>> graph = DirectedGraph(edges=[("a","b"),("c","b"),("d","a"),("b","d"),("c","a"),("d","c"),("c","f"),("f","d"),("e",None)])
>>> print(graph)
   a  b  c  d  e  f  
a     *              
b           *        
c  *  *           *  
d  *     *           
e                    
f           *        

>>> graph.bfs_path_value("a")
{'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4}
>>> graph.dijkstra("a")
{'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4}
>>> graph.spfa("a")
{'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4}
>>> graph.floyd()
{
    'a': {'a': 0,   'b': 1,   'c': 3,   'd': 2,   'e': inf, 'f': 4, },
    'b': {'a': 2,   'b': 0,   'c': 2,   'd': 1,   'e': inf, 'f': 3, },
    'c': {'a': 1,   'b': 1,   'c': 0,   'd': 2,   'e': inf, 'f': 1, },
    'd': {'a': 1,   'b': 2,   'c': 1,   'd': 0,   'e': inf, 'f': 2, },
    'f': {'a': 2,   'b': 3,   'c': 2,   'd': 1,   'e': inf, 'f': 0, },
    'e': {'a': inf, 'b': inf, 'c': inf, 'd': inf, 'e': 0,   'f': inf}
}
>>> for n in ["a", "b", "c", "d", "e", "f"]:
...     p = graph.dfs_path_value("a", n)
...     print(p, end=", ")
...
0, 1, 3, 2, inf, 4, 
```
### Weighted

```
>>> from ezcode.graph.directed import DirectedGraph
>>> graph = DirectedGraph(
...     edges=[("a","b"),("c","b"),("d","a"),("b","d"),("c","a"),("d","c"),("c","f"),("f","d"),("e",None)],
...     weights=[0.8, 0.7, 0.6, 0.8, 0.5, 0.8, 0.6, 0.4, None]
... )
>>> print(graph)
      a     b     c     d     e     f     
a           0.8                           
b                       0.8               
c     0.5   0.7                     0.6   
d     0.6         0.8                     
e                                         
f                       0.4               

>>> graph.dijkstra("a")
{'a': 0, 'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3}
>>> graph.spfa("a")
{'a': 0, 'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3}
>>> graph.floyd()
{
    'a': {'a': 0,   'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3.0,},
    'b': {'a': 1.4, 'b': 0,   'c': 1.6, 'd': 0.8, 'e': inf, 'f': 2.2,},
    'c': {'a': 0.5, 'b': 0.7, 'c': 0,   'd': 1.0, 'e': inf, 'f': 0.6,},
    'd': {'a': 0.6, 'b': 1.4, 'c': 0.8, 'd': 0,   'e': inf, 'f': 1.4,},
    'e': {'a': inf, 'b': inf, 'c': inf, 'd': inf, 'e': 0,   'f': inf,},
    'f': {'a': 1.0, 'b': 1.8, 'c': 1.2, 'd': 0.4, 'e': inf, 'f': 0,  }
}
>>> for n in ["a", "b", "c", "d", "e", "f"]:
...     p = graph.dfs_path_value("a", n)
...     print(p, end=", ")
... 
0, 0.8, 2.4, 1.6, inf, 3.0, 

>>> graph.dijkstra("a", self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{'a': 1, 'b': 0.8, 'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072}
>>> graph.spfa("a", self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{'a': 1, 'b': 0.8, 'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072}
>>> graph.floyd(self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{
    'a': {'a': 1,    'b': 0.8,   'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072},
    'b': {'a': 0.48, 'b': 1,     'c': 0.64,  'd': 0.8,  'e': 0, 'f': 0.384 },
    'c': {'a': 0.5,  'b': 0.7,   'c': 1,     'd': 0.56, 'e': 0, 'f': 0.6   },
    'd': {'a': 0.6,  'b': 0.56,  'c': 0.8,   'd': 1,    'e': 0, 'f': 0.48  },
    'e': {'a': 0,    'b': 0,     'c': 0,     'd': 0,    'e': 1, 'f': 0     },
    'f': {'a': 0.24, 'b': 0.224, 'c': 0.32,  'd': 0.4,  'e': 0, 'f': 1     }
}
>>> for n in ["a", "b", "c", "d", "e", "f"]:
...     p = graph.dfs_path_value("a", n, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
...     print(p, end=", ")
...
1, 0.8, 0.512, 0.64, 0, 0.3072, 
```

# Undirected Graph

## Shortest Path Algorithm

### Unweighted

```
>>> from ezcode.graph.undirected import UndirectedGraph
>>> graph = UndirectedGraph(edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]])
>>> print(graph)
   A  B  C  D  E  
A     *  *        
B  *     *  *     
C  *  *     *  *  
D     *  *     *  
E        *  *     

>>> graph.bfs_path_value("A")
{'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2}
>>> graph.dijkstra("A")
{'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2}
>>> graph.spfa("A")
{'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2}
>>> graph.floyd()
{
    'A': {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2},
    'B': {'A': 1, 'B': 0, 'C': 1, 'D': 1, 'E': 2},
    'C': {'A': 1, 'B': 1, 'C': 0, 'D': 1, 'E': 1},
    'D': {'A': 2, 'B': 1, 'C': 1, 'D': 0, 'E': 1},
    'E': {'A': 2, 'B': 2, 'C': 1, 'D': 1, 'E': 0}
}
>>> for n in ["A", "B", "C", "D", "E"]:
...     p = graph.dfs_path_value("A", n)
...     print(p, end=", ")
... 
0, 1, 1, 2, 2,
```

### Weighted

```
>>> from ezcode.graph.undirected import UndirectedGraph
>>> graph = UndirectedGraph(edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]], weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3])
>>> print(graph)
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       

>>> graph.dijkstra("A")
{'A': 0, 'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0}
>>> graph.spfa("A")
{'A': 0, 'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0}
>>> graph.floyd()
{
    'A': {'A': 0,   'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0},
    'B': {'A': 0.7, 'B': 0,   'C': 0.5, 'D': 0.9, 'E': 1.2},
    'C': {'A': 0.2, 'B': 0.5, 'C': 0,   'D': 0.9, 'E': 0.8},
    'D': {'A': 1.1, 'B': 0.9, 'C': 0.9, 'D': 0,   'E': 0.3},
    'E': {'A': 1.0, 'B': 1.2, 'C': 0.8, 'D': 0.3, 'E': 0  }
}
>>> for n in ["A", "B", "C", "D", "E"]:
...     p = graph.dfs_path_value("A", n)
...     print(p, end=", ")
... 
0, 0.7, 0.2, 1.1, 1.0, 

>>> graph.dijkstra("A", self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{'A': 1, 'B': 0.8, 'C': 0.648, 'D': 0.72, 'E': 0.5184}
>>> graph.spfa("A", self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{'A': 1, 'B': 0.8, 'C': 0.648, 'D': 0.72, 'E': 0.5184}
>>> graph.floyd(self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
{
    'A': {'A': 1,      'B': 0.8,   'C': 0.648, 'D': 0.72, 'E': 0.5184},
    'B': {'A': 0.8,    'B': 1,     'C': 0.81,  'D': 0.9,  'E': 0.648 },
    'C': {'A': 0.648,  'B': 0.81,  'C': 1,     'D': 0.9,  'E': 0.8   },
    'D': {'A': 0.72,   'B': 0.9,   'C': 0.9,   'D': 1,    'E': 0.72  },
    'E': {'A': 0.5184, 'B': 0.648, 'C': 0.8,   'D': 0.72, 'E': 1     }
}
>>> for n in ["A", "B", "C", "D", "E"]:
...     p = graph.dfs_path_value("A", n, self_loop_weight=1, disconnected_edge_weight=0, path_value_func=lambda a,b: a*b, min_max_func=max)
...     print(p, end=", ")
... 
1, 0.8, 0.648, 0.72, 0.5184,
```

## Detect Negative Cycle

```
>>> from ezcode.graph.directed import DirectedGraph
>>> graph = DirectedGraph(
...     edges=[["A","B"],["B","C"],["C","D"],["D","B"]],
...     weights=[3, 1, -3, 1]
... )
>>> print(graph)
    A   B   C   D   
A       3           
B           1       
C               -3  
D       1           

>>> graph.spfa("A", check_cycle=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.9/site-packages/ezcode/graph/__init__.py", line 129, in spfa
    raise NegativeCycleExist()
ezcode.graph.NegativeCycleExist

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

>>> graph.spfa("A", check_cycle=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zgao/Desktop/study/ez_code/src/ezcode/graph/undirected.py", line 114, in spfa
    raise NegativeCycleExist()
ezcode.graph.NegativeCycleExist
```
