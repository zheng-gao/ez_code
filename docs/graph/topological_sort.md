# Topological Sort

```python
    """
    a <──────────── c
    │               │
    │               │
    v               v
    d ────> b ────> f ────> e
    """
>>> from ezcode.graph.directed import DirectedGraph
>>> dag = DirectedGraph(edges=[("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")])
>>> dag.print()
   a  b  c  d  e  f  
a           *        
b                 *  
c  *              *  
d     *              
e                    
f              *     
>>> print(dag.topological_order())
['e', 'f', 'b', 'd', 'a', 'c']
>>> dag.is_acyclic()
True

    """
    a <──── d
    │       ^
    │       │
    v       │
    b ────> c
    """
>>> circular_dependencies = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]
>>> DirectedGraph(edges=circular_dependencies).is_acyclic()
False
```