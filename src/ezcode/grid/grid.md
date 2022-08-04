## A* Shortest Path Algorithm
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

1111100
100S222
0011012
1222222
0211000
02D0011
0110010

>>> path = grid.bfs(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])

1111100
122S000
0211010
1200000
0211000
02D0011
0110010
 
>>> path = grid.dijkstra(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])

1111100
122S000
0211010
1200000
0211000
02D0011
0110010

>>> path = grid.a_star(source, destination, valid_values)
>>> grid.print(layers=[
...     {"value": "2", "nodes": path},
...     {"value": "S", "nodes": [source]},
...     {"value": "D", "nodes": [destination]},
... ])

1111100
100S200
0011210
1000200
0011200
00D2211
0110010

>>> paths = grid.dfs_backtracking(source, destination, valid_values)
>>> i, layers = 2, list()
>>> for p in paths:
...     layers.append({"value": i, "nodes": p})
...     i += 1
... 
>>> layers.append({"value": i, "nodes": [source, destination]})
>>> grid.print(layers=layers)

1111100
1224300
0211310
1200300
0211300
0243311
0110010           
```
