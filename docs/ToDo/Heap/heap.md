## Priority Queue

### Min Priority Queue

```python
>>> from ezcode.heap import PriorityQueue
>>> min_pq = PriorityQueue()
>>> for data in [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]:
...     min_pq.push(data)
...     print(min_pq.top(with_priority=True))
... 
('D', 4)
('C', 3)
('C', 3)
('A', 1)
('A', 1)

>>> while len(min_pq) > 0:
...     print(min_pq.pop(with_priority=True))
... 
('A', 1)
('B', 2)
('C', 3)
('D', 4)
('E', 5)
```

### Max Priority Queue

```python
>>> from ezcode.heap import PriorityQueue
>>> max_pq = PriorityQueue(reverse=True)
>>> for data in [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]:
...     max_pq.push(data)
...     print(max_pq.top(with_priority=True))
... 
('D', 4)
('D', 4)
('E', 5)
('E', 5)
('E', 5)

>>> while len(max_pq) > 0:
...     print(max_pq.pop(with_priority=True))
... 
('E', 5)
('D', 4)
('C', 3)
('B', 2)
('A', 1)
```

## Priority Map

### Min Priority Map

```python
>>> from ezcode.heap import PriorityMap
>>> min_map = PriorityMap()
>>> for data in [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]:
...     min_map.push(data)
...     min_map.top(with_priority=True)
... 
('D', 4)
('C', 3)
('C', 3)
('A', 1)
('A', 1)

>>> for key in ["B", "F"]:
...     print(f"{key} in min_map: {key in min_map}")
... 
B in min_map: True
F in min_map: False

>>> min_map["C"]
3
>>> min_map.update("E", 0)
>>> min_map.top(with_priority=True)
('E', 0)
>>> min_map["B"] = 6
>>> del min_map["C"]
>>> while len(min_map) > 0:
...     min_map.pop(with_priority=True)
... 
('E', 0)
('A', 1)
('D', 4)
('B', 6)

>>> print(PriorityMap({"A": 1, "B": 2, "C": 3}))
[('A', 1), ('B', 2), ('C', 3)]
```

### Max Priority Map

```python
>>> from ezcode.heap import PriorityMap
>>> max_map = PriorityMap(reverse=True)
>>> for data in [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]:
...     max_map.push(data)
...     max_map.top(with_priority=True)
... 
('D', 4)
('D', 4)
('E', 5)
('E', 5)
('E', 5)

>>> for key in ["B", "F"]:
...     print(f"{key} in max_map: {key in max_map}")
... 
B in max_map: True
F in max_map: False

>>> max_map["C"]
3
>>> 
>>> max_map.update("E", 0)
>>> max_map.top(with_priority=True)
('D', 4)
>>> max_map["B"] = 6
>>> del min_map["C"]
>>> while len(max_map) > 0:
...     max_map.pop(with_priority=True)
... 
('B', 6)
('D', 4)
('A', 1)
('E', 0)

>>> print(PriorityMap({"A": 1, "B": 2, "C": 3}, reverse=True))
[('C', 3), ('A', 1), ('B', 2)]
```
