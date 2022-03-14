## Priority Queue

### Min Priority Queue

```python
>>> from ezcode.heap.priority_queue import PriorityQueue
>>> min_pq = PriorityQueue()
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     min_pq.push(data)
...     print(min_pq.peek())
... 
(4, 'D')
(3, 'C')
(3, 'C')
(1, 'A')
(1, 'A')

>>> while len(min_pq) > 0:
...     print(min_pq.pop())
... 
(1, 'A')
(2, 'B')
(3, 'C')
(4, 'D')
(5, 'E')
```

### Max Priority Queue

```python
>>> max_pq = PriorityQueue(min_heap=False)
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     max_pq.push(data)
...     print(max_pq.peek())
... 
(4, 'D')
(4, 'D')
(5, 'E')
(5, 'E')
(5, 'E')

>>> while len(max_pq) > 0:
...     print(max_pq.pop())
... 
(5, 'E')
(4, 'D')
(3, 'C')
(2, 'B')
(1, 'A')
```

## Priority Map

### Min Priority Map

```python
>>> from ezcode.array.heap import PriorityMap
>>> min_map = PriorityMap()
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     min_map.push(data)
...     min_map.peek()
... 
(4, 'D')
(3, 'C')
(3, 'C')
(1, 'A')
(1, 'A')

>>> for key in ["B", "F"]:
...     print(f"{key} in min_map: {key in min_map}")
... 
B in min_map: True
F in min_map: False

>>> min_map.get_priority("C")
3
>>> min_map.update((0, "E"))
>>> min_map.peek()
(0, 'E')
>>> min_map.update((6, "B"))
>>> min_map.delete("C")
>>> while len(min_map) > 0:
...     min_map.pop()
... 
(0, 'E')
(1, 'A')
(4, 'D')
(6, 'B')

>>> print(PriorityMap({"A": 1, "B": 2, "C": 3}))
[(1, 'A'), (2, 'B'), (3, 'C')]
```

### Max Priority Map

```python
>>> from ezcode.array.heap import PriorityMap
>>> max_map = PriorityMap(min_heap=False)
>>> for data in [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]:
...     max_map.push(data)
...     max_map.peek()
... 
(4, 'D')
(4, 'D')
(5, 'E')
(5, 'E')
(5, 'E')

>>> for key in ["B", "F"]:
...     print(f"{key} in max_map: {key in max_map}")
... 
B in max_map: True
F in max_map: False

>>> max_map.get_priority("C")
3
>>> 
>>> max_map.update((0, "E"))
>>> max_map.peek()
(4, 'D')
>>> max_map.update((6, "B"))
>>> min_map.delete("C")
>>> while len(max_map) > 0:
...     max_map.pop()
... 
(6, 'B')
(4, 'D')
(1, 'A')
(0, 'E')

>>> print(PriorityMap({"A": 1, "B": 2, "C": 3}, min_heap=False))
[(3, 'C'), (1, 'A'), (2, 'B')]
```

## BlockingPriorityQueue

```python
>>> from random import randrange
>>> from threading import Thread, current_thread
>>> from multiprocessing.pool import ThreadPool
>>> from ezcode.heap import BlockingPriorityQueue
>>> 
>>> 
>>> def produce(queue, stop):
...     t = current_thread()
...     for _ in range(stop):
...         random_int = randrange(stop)
...         print(f"[{t.name}-{t.native_id}] Pushing {random_int}")
...         queue.push(random_int)
...         print(f"[{t.name}-{t.native_id}] Pushed {random_int}")
... 
>>> def consume(queue):
...     t = current_thread()
...     while True:
...         print(f"[{t.name}-{t.native_id}] Try Poping ...")
...         data = queue.pop()
...         print(f"[{t.name}-{t.native_id}] Poped {data}")
... 
>>> queue = BlockingPriorityQueue()
>>> producers = [Thread(target=produce, args=(queue, 5), name="Producer") for _ in range(1)]
>>> consumers = [Thread(target=consume, args=(queue,), name="Consumer") for _ in range(1)]
>>> for t in consumers + producers:
...     t.start()
... 
[Consumer-1259272] Try Poping ...
[Producer-1259273] Pushing 4
[Producer-1259273] Pushed 4
[Consumer-1259272] Poped 4
[Producer-1259273] Pushing 2
[Consumer-1259272] Try Poping ...
[Consumer-1259272] Poped 2
[Consumer-1259272] Try Poping ...
[Producer-1259273] Pushed 2
[Producer-1259273] Pushing 1
[Producer-1259273] Pushed 1
[Producer-1259273] Pushing 3
[Producer-1259273] Pushed 3
[Producer-1259273] Pushing 3
[Producer-1259273] Pushed 3
[Consumer-1259272] Poped 1
[Consumer-1259272] Try Poping ...
[Consumer-1259272] Poped 3
[Consumer-1259272] Try Poping ...
[Consumer-1259272] Poped 3
[Consumer-1259272] Try Poping ...
```
