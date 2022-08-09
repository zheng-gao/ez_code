## Grid Iterator
```python
>>> from ezcode.grid.iterator import GridIteratorFactory
>>> grid = [
...     [1, 2, 3],
...     [8, 9, 4],
...     [7, 6, 5]
... ]

>>> for data in GridIteratorFactory.get(grid, 1, 0, iterator="horizontal"):
...     print(data, end=" ")
... 
8 9 4

>>> for data in GridIteratorFactory.get(grid, 2, 2, iterator="vertical", reverse=True):
...     print(data, end=" ")
... 
5 4 3

>>> for data in GridIteratorFactory.get(grid, 0, 0, iterator="major_diagonal"):
...     print(data, end=" ")
... 
1 9 5

>>> for data in GridIteratorFactory.get(grid, 0, 2, iterator="minor_diagonal", reverse=True):
...     print(data, end=" ")
... 
3 9 7

>>> for data in GridIteratorFactory.get(grid, 0, 0, iterator="spiral"):
...     print(data, end=" ")
... 
1 2 3 4 5 6 7 8 9

>>> for data in GridIteratorFactory.get(grid, 0, 2, row_end=1, col_end=2, iterator="spiral", reverse=True):
...     print(data, end=" ")
... 
3 2 1 8 7 6 5 4
```

## Path Finder
```python
>>> from ezcode.grid import Grid
>>> grid = Grid(
...     [
...         [1, 1, 1, 1, 1, 0, 0],
...         [1, 0, 0, 0, 0, 0, 0],
...         [0, 0, 1, 1, 0, 1, 0],
...         [1, 0, 0, 0, 0, 0, 0],
...         [0, 0, 1, 1, 0, 0, 0],
...         [0, 0, 0, 0, 0, 1, 1],
...         [0, 1, 1, 0, 0, 1, 0]
...     ]
... )
>>> 
>>> source, destination, valid_values = (1, 3), (5, 2), set([0])
>>> 
>>> path = grid.dfs(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])
"""
1111100
100S222
0011012
1222222
0211000
02D0011
0110010
"""
>>> path = grid.bfs(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])
"""
1111100
122S000
0211010
1200000
0211000
02D0011
0110010
"""
>>> path = grid.dijkstra(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])
"""
1111100
122S000
0211010
1200000
0211000
02D0011
0110010
"""
>>> path = grid.a_star(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])
"""
1111100
100S200
0011210
1000200
0011200
00D2211
0110010
"""
>>> paths = grid.dfs_backtracking(source, destination, valid_values)
>>> i, layers = 2, list()
>>> for p in paths:
...     layers.append({"value": i, "nodes": p})
... 
>>> layers.append({"value": "S", "nodes": [source]})
>>> layers.append({"value": "D", "nodes": [destination]})
>>> grid.print(layers=layers)
"""
1111100
122S300
0211310
1200300
0211300
02D3311
0110010
"""         
```
