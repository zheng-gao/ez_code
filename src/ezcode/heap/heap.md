## Priority Queue

### Min P-Queue

```
>>> from ezcode.heap.priority_queue import PriorityQueue
>>> min_q = PriorityQueue()
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     min_q.push(data)
...     print(min_q.peek())
... 
(4, 'D')
(3, 'C')
(3, 'C')
(1, 'A')
(1, 'A')

>>> while len(min_q) > 0:
...     print(min_q.pop())
... 
(1, 'A')
(2, 'B')
(3, 'C')
(4, 'D')
(5, 'E')
```

### Max P-Queue

```
>>> max_q = PriorityQueue(min_heap=False)
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     max_q.push(data)
...     print(max_q.peek())
... 
(4, 'D')
(4, 'D')
(5, 'E')
(5, 'E')
(5, 'E')

>>> while len(max_q) > 0:
...     print(max_q.pop())
... 
(5, 'E')
(4, 'D')
(3, 'C')
(2, 'B')
(1, 'A')
```
