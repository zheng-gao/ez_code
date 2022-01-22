# Directed Acyclic Graph

## Topological Sort

```
>>> from ezcode.graph.directed_acyclic_graph import ActivityOnVertexGraph
>>> dependencies = [("c", "a"), ("b", "e"), ("a", "d"), ("c", "e"), ("d", "b")]
>>> aov_graph = ActivityOnVertexGraph(dependencies)
>>> aov_graph.print()
  a b c d e 
a       *   
b         * 
c *       * 
d   *       
e 
>>> print(aov_graph.topological_order())
['e', 'b', 'd', 'a', 'c']
>>> aov_graph.is_directed_acyclic_graph()
True
>>> circular_dependencies = [("a", "b"), ("b", "a")]
>>> ActivityOnVertexGraph(circular_dependencies).is_directed_acyclic_graph()
False
```