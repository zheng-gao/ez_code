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
>>> grid.print()

1111100
1000000
0011010
1000000
0011000
0000011
0110010

>>> value_color = {0: "White", 1: "Red", 2: "Green", 3: "Yellow", 4: "Blue"}
>>> grid.print(value_color)
              
              
              
              
              
              
              

>>> source, destination, valid_values = (1, 3), (5, 2), set([0])
>>> path = grid.dfs(source, destination, valid_values)
>>> grid.print(value_color, [{"value": 3, "nodes": path}, {"value": 4, "nodes": [source, destination]}])
              
              
              
              
              
              
              

>>> path = grid.bfs(source, destination, valid_values)
>>> grid.print(value_color, [{"value": 3, "nodes": path}, {"value": 4, "nodes": [source, destination]}])
              
              
              
              
              
              
              

>>> path = grid.dijkstra(source, destination, valid_values)
>>> grid.print(value_color, [{"value": 3, "nodes": path}, {"value": 4, "nodes": [source, destination]}])
              
              
              
              
              
              
              

>>> path = grid.a_star(source, destination, valid_values)
>>> grid.print(value_color, [{"value": 3, "nodes": path}, {"value": 4, "nodes": [source, destination]}])
              
              
              
              
              
              
              

>>> paths = grid.dfs_backtracking(source, destination, valid_values)
>>> i, layers = 2, list()
>>> for p in paths:
...     layers.append({"value": i, "nodes": p})
...     i += 1
... 
>>> layers.append({"value": i, "nodes": [source, destination]})
>>> grid.print(value_color, layers)
              
              
              
              
              
              
              
```
