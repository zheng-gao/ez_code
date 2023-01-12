# Eulerian Path
## Undirected Graph
```python
    """
    A ────── C
    │       ╱│╲
    │      ╱ │ ╲
    │     ╱  │  ╲
    │    ╱   │   E
    │   ╱    │  ╱
    │  ╱     │ ╱
    │ ╱      │╱
    B ────── D
    """
>>> from ezcode.graph.undirected import UndirectedGraph
>>> graph = UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "E"]])
>>> print(graph.eulerian_path())
['B', 'A', 'C', 'B', 'D', 'C', 'E', 'D']
>>> print(graph.eulerian_path(start_node="D"))
['D', 'B', 'A', 'C', 'D', 'E', 'C', 'B']
>>> print(graph.eulerian_path(start_node="A"))
None
>>> print(graph.eulerian_path(start_node="E"))
None

    """
    A ── B
    │ ╲
    │  ╲
    D   C
    """
>>> print(UndirectedGraph(edges=[["A", "B"], ["A", "C"], ["A", "D"]]).eulerian_path())
None
```
## Directed Graph
```python
    """
    A <─── B 
    │      ^
    │      │
    v      │
    D ───> C <─── E
           │
           v
           F
    """
>>> from ezcode.graph.directed import DirectedGraph
>>> graph = DirectedGraph(edges=[["B", "A"], ["A", "D"], ["D", "C"], ["C", "B"], ["E", "C"], ["C", "F"]])
>>> print(graph.eulerian_path())
['E', 'C', 'B', 'A', 'D', 'C', 'F']
>>> print(graph.eulerian_path(start_node="E"))
['E', 'C', 'B', 'A', 'D', 'C', 'F']
>>> print(graph.eulerian_path(start_node="A"))
None

    """
    A <─── B ───> F
    │      ^
    │      │
    v      │
    D ───> C <─── E
    """
>>> graph = DirectedGraph(edges=[["B", "A"], ["A", "D"], ["D", "C"], ["C", "B"], ["E", "C"], ["B", "F"]])
>>> print(graph.eulerian_path())
None
```
