# Directed Graph

## Shortest Path Algorithm

### Unweighted
```python
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
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> edges=[("a","b"),("c","b"),("d","a"),("b","d"),("c","a"),("d","c"),("c","f"),("f","d"),("e",None)]
>>> path_finder = GraphPathFinder(is_directed=True, edges=edges)
>>> path_finder.print()
   a  b  c  d  e  f  
a     *              
b           *        
c  *  *           *  
d  *     *           
e                    
f           *        

>>> path_finder.bfs("a")
(None, {'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4})
>>> path_finder.dijkstra("a")
(None, {'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4})
>>> path_finder.spfa("a")
(None, {'a': 0, 'b': 1, 'c': 3, 'd': 2, 'e': inf, 'f': 4})
>>> path_finder.floyd()
{
    'a': {'a': 0,   'b': 1,   'c': 3,   'd': 2,   'e': inf, 'f': 4, },
    'b': {'a': 2,   'b': 0,   'c': 2,   'd': 1,   'e': inf, 'f': 3, },
    'c': {'a': 1,   'b': 1,   'c': 0,   'd': 2,   'e': inf, 'f': 1, },
    'd': {'a': 1,   'b': 2,   'c': 1,   'd': 0,   'e': inf, 'f': 2, },
    'f': {'a': 2,   'b': 3,   'c': 2,   'd': 1,   'e': inf, 'f': 0, },
    'e': {'a': inf, 'b': inf, 'c': inf, 'd': inf, 'e': 0,   'f': inf}
}
>>> path_finder.bfs("c", "d")
(2, ['c', 'b', 'd'])
>>> path_finder.dijkstra("c", "d")
(2, ['c', 'b', 'd'])
>>> path_finder.spfa("c", "d")
(2, ['c', 'b', 'd'])
>>> path_finder.backtracking("c", "d")
(2, [['c', 'b', 'd'], ['c', 'f', 'd']])
```
### Weighted

```python
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
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> path_finder = GraphPathFinder(
...     is_directed=True,
...     edges=[("a","b"),("c","b"),("d","a"),("b","d"),("c","a"),("d","c"),("c","f"),("f","d"),("e",None)],
...     weights=[0.8, 0.7, 0.6, 0.8, 0.5, 0.8, 0.6, 0.4, None]
... )
>>> path_finder.print()
      a     b     c     d     e     f     
a           0.8                           
b                       0.8               
c     0.5   0.7                     0.6   
d     0.6         0.8                     
e                                         
f                       0.4               

>>> path_finder.dijkstra("a")
(None, {'a': 0, 'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3.0})
>>> path_finder.spfa("a")
(None, {'a': 0, 'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3.0})
>>> path_finder.floyd()
{
    'a': {'a': 0,   'b': 0.8, 'c': 2.4, 'd': 1.6, 'e': inf, 'f': 3.0,},
    'b': {'a': 1.4, 'b': 0,   'c': 1.6, 'd': 0.8, 'e': inf, 'f': 2.2,},
    'c': {'a': 0.5, 'b': 0.7, 'c': 0,   'd': 1.0, 'e': inf, 'f': 0.6,},
    'd': {'a': 0.6, 'b': 1.4, 'c': 0.8, 'd': 0,   'e': inf, 'f': 1.4,},
    'e': {'a': inf, 'b': inf, 'c': inf, 'd': inf, 'e': 0,   'f': inf,},
    'f': {'a': 1.0, 'b': 1.8, 'c': 1.2, 'd': 0.4, 'e': inf, 'f': 0,  }
}
>>> path_finder.dijkstra("f", "b")
(1.8, ['f', 'd', 'a', 'b'])
>>> path_finder.spfa("f", "b")
(1.8, ['f', 'd', 'a', 'b'])
>>> path_finder.backtracking("f", "b")
(1.8, [['f', 'd', 'a', 'b']])

>>> config = {"self_loop_weight": 1, "disconnected_edge_weight": 0, "path_value_func": (lambda a,b: a * b), "is_min": False}
>>> path_finder.dijkstra("a", **config)
{'a': 1, 'b': 0.8, 'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072}
>>> path_finder.spfa("a", **config)
{'a': 1, 'b': 0.8, 'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072}
>>> path_finder.floyd(**config)
{
    'a': {'a': 1,    'b': 0.8,   'c': 0.512, 'd': 0.64, 'e': 0, 'f': 0.3072},
    'b': {'a': 0.48, 'b': 1,     'c': 0.64,  'd': 0.8,  'e': 0, 'f': 0.384 },
    'c': {'a': 0.5,  'b': 0.7,   'c': 1,     'd': 0.56, 'e': 0, 'f': 0.6   },
    'd': {'a': 0.6,  'b': 0.56,  'c': 0.8,   'd': 1,    'e': 0, 'f': 0.48  },
    'e': {'a': 0,    'b': 0,     'c': 0,     'd': 0,    'e': 1, 'f': 0     },
    'f': {'a': 0.24, 'b': 0.224, 'c': 0.32,  'd': 0.4,  'e': 0, 'f': 1     }
}
>>> path_finder.dijkstra("f", "b", **config)
(0.224, ['f', 'd', 'c', 'b'])
>>> path_finder.spfa("f", "b", **config)
(0.224, ['f', 'd', 'c', 'b'])
>>> path_finder.backtracking("f", "b", **config)
(0.224, [['f', 'd', 'c', 'b']])
```

## Detect Negative Cycle

```python
    """
    A ─3─> B
         ^ │
        ╱  │
       ╱  -4
      2    │
     ╱     v
    D <─1─ C
    """
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> path_finder = GraphPathFinder(
...     is_directed=True,
...     edges=[["A","B"],["B","C"],["C","D"],["D","B"]],
...     weights=[3, -4, 1, 2]
... )
>>> path_finder.print()
    A   B   C   D   
A       3           
B           -4      
C               1   
D       2           

>>> path_finder.spfa("A", check_cycle=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zgao/Desktop/code/ez_code/src/ezcode/graph/pathfinder.py", line 165, in spfa
    raise NegativeCycleExistError()
ezcode.graph.pathfinder.NegativeCycleExistError

    """
          D ────┐
         ╱│     │
        ╱ │     │
       1  2     │
      ╱   │     │
     ╱    │     │
    B ─2─ A     1
     ╲    │     │
      ╲   │     │
      -3  3     │
        ╲ │     │
         ╲│     │
          C ────┘
    """
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> path_finder = GraphPathFinder(
...     is_directed=False,
...     edges=[["A","B"],["A","C"],["A","D"],["B","C"],["B","D"],["C","D"]],
...     weights=[2, 3, 2, -3, 1, 1]
... )
>>> path_finder.print()
    A   B   C   D   
A       2   3   2   
B   2       -3  1   
C   3   -3      1   
D   2   1   1       

>>> path_finder.spfa("A", check_cycle=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zgao/Desktop/code/ez_code/src/ezcode/graph/pathfinder.py", line 165, in spfa
    raise NegativeCycleExistError()
ezcode.graph.pathfinder.NegativeCycleExistError
```

# Undirected Graph

## Shortest Path Algorithm

### Unweighted

```python
    """
    A ─── C ─── E
     ╲    │╲    │
      ╲   │ ╲   │
       ╲  │  ╲  │
        ╲ │   ╲ │
         ╲│    ╲│
          B ─── D
    """
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> path_finder = GraphPathFinder(
...     is_directed=False,
...     edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]]
... )
>>> path_finder.print()
   A  B  C  D  E  
A     *  *        
B  *     *  *     
C  *  *     *  *  
D     *  *     *  
E        *  *     

>>> path_finder.bfs("A")
(None, {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2})
>>> path_finder.dijkstra("A")
(None, {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2})
>>> path_finder.spfa("A")
(None, {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2})
>>> path_finder.floyd()
{
    'A': {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2},
    'B': {'A': 1, 'B': 0, 'C': 1, 'D': 1, 'E': 2},
    'C': {'A': 1, 'B': 1, 'C': 0, 'D': 1, 'E': 1},
    'D': {'A': 2, 'B': 1, 'C': 1, 'D': 0, 'E': 1},
    'E': {'A': 2, 'B': 2, 'C': 1, 'D': 1, 'E': 0}
}
>>> path_finder.bfs("A", "D")
(2, ['A', 'B', 'D'])
>>> path_finder.dijkstra("A", "D")
(2, ['A', 'B', 'D'])
>>> path_finder.spfa("A", "D")
(2, ['A', 'B', 'D'])
>>> path_finder.backtracking("A", "D")
(2, [['A', 'B', 'D'], ['A', 'C', 'D']])
```

### Weighted

```python
    """
    A ─0.2─ C ─0.8─ E
     ╲      │╲      │
      ╲     │ ╲     │
      0.8   │  ╲   0.3
        ╲  0.5  ╲   │
         ╲  │   0.9 │
          ╲ │     ╲ │
            B ─0.9─ D
    """
>>> from ezcode.graph.pathfinder import GraphPathFinder
>>> path_finder = GraphPathFinder(
...     is_directed=False,
...     edges=[["A","B"],["A","C"],["B","C"],["B","D"],["C","D"],["C","E"],["D","E"]],
...     weights=[0.8, 0.2, 0.5, 0.9, 0.9, 0.8, 0.3]
... )
>>> path_finder.print()
     A    B    C    D    E    
A         0.8  0.2            
B    0.8       0.5  0.9       
C    0.2  0.5       0.9  0.8  
D         0.9  0.9       0.3  
E              0.8  0.3       

>>> path_finder.dijkstra("A")
(None, {'A': 0, 'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0})
>>> path_finder.spfa("A")
(None, {'A': 0, 'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0})
>>> path_finder.floyd()
{
    'A': {'A': 0,   'B': 0.7, 'C': 0.2, 'D': 1.1, 'E': 1.0},
    'B': {'A': 0.7, 'B': 0,   'C': 0.5, 'D': 0.9, 'E': 1.2},
    'C': {'A': 0.2, 'B': 0.5, 'C': 0,   'D': 0.9, 'E': 0.8},
    'D': {'A': 1.1, 'B': 0.9, 'C': 0.9, 'D': 0,   'E': 0.3},
    'E': {'A': 1.0, 'B': 1.2, 'C': 0.8, 'D': 0.3, 'E': 0  }
}
>>> path_finder.dijkstra("A", "D")
(1.1, ['A', 'C', 'D'])
>>> path_finder.spfa("A", "D")
(1.1, ['A', 'C', 'D'])
>>> path_finder.backtracking("A", "D")
(1.1, [['A', 'C', 'D']])

>>> config = {"self_loop_weight": 1, "disconnected_edge_weight": 0, "path_value_func": (lambda a,b: a * b), "is_min": False}
>>> path_finder.dijkstra("A", **config)
(None, {'A': 1, 'B': 0.8, 'C': 0.648, 'D': 0.72, 'E': 0.5184})
>>> path_finder.spfa("A", **config)
(None, {'A': 1, 'B': 0.8, 'C': 0.648, 'D': 0.72, 'E': 0.5184})
>>> path_finder.floyd(**config)
{
    'A': {'A': 1,      'B': 0.8,   'C': 0.648, 'D': 0.72, 'E': 0.5184},
    'B': {'A': 0.8,    'B': 1,     'C': 0.81,  'D': 0.9,  'E': 0.648 },
    'C': {'A': 0.648,  'B': 0.81,  'C': 1,     'D': 0.9,  'E': 0.8   },
    'D': {'A': 0.72,   'B': 0.9,   'C': 0.9,   'D': 1,    'E': 0.72  },
    'E': {'A': 0.5184, 'B': 0.648, 'C': 0.8,   'D': 0.72, 'E': 1     }
}
>>> path_finder.dijkstra("A", "D", **config)
(0.72, ['A', 'B', 'D'])
>>> path_finder.spfa("A", "D", **config)
(0.72, ['A', 'B', 'D'])
>>> path_finder.backtracking("A", "D", **config)
(0.72, [['A', 'B', 'D']])
```

