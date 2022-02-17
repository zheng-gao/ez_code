## Priority Queue

### Min P-Queue

```
>>> from ezcode.heap.priority_queue import PriorityQueue
>>> min_q = PriorityQueue()
>>> for data in [4, 3, 5, 1, 2]:
...     min_q.push(data)
...     print(min_q.peek())
... 
4
3
3
1
1
>>> while len(min_q) > 0:
...     print(min_q.pop())
... 
1
2
3
4
5
```

### Max P-Queue

```
>>> max_q = PriorityQueue(is_min=False)
>>> for data in [4, 3, 5, 1, 2]:
...     max_q.push(data)
...     print(max_q.peek())
... 
4
4
5
5
5
>>> while len(max_q) > 0:
...     print(max_q.pop())
... 
5
4
3
2
1
```
