# Directed Acyclic Graph

## Topological Sort

```
>>> from ezcode.graph.directed_acyclic_graph import ActivityOnVertexGraph
>>> dependencies = [("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")]
>>> aov_graph = ActivityOnVertexGraph(dependencies)
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
>>> ActivityOnVertexGraph(circular_dependencies).is_directed_acyclic_graph()
False
```