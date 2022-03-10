## SinglyLinkedList

```
>>> from ezcode.list.linked_list import SinglyLinkedList
>>> class Node:
...     def __init__(self, v=None, n=None):
...         self.v = v
...         self.n = n
... 
>>> head = Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7))))))))
>>> s_list = SinglyLinkedList(head=head, data_name="v", next_name="n")
>>> print(s_list)
0 ─> 1 ─> 2 ─> 3 ─> 4 ─> 5 ─> 6 ─> 7 ─> None
>>> c_list = s_list.copy()
>>> print(c_list)
0 ─> 1 ─> 2 ─> 3 ─> 4 ─> 5 ─> 6 ─> 7 ─> None
>>> c_list.reverse(start_index=2, end_index=5)
>>> print(c_list)
0 ─> 1 ─> 5 ─> 4 ─> 3 ─> 2 ─> 6 ─> 7 ─> None
>>> s_list.reverse(start_index=4)
>>> print(s_list)
0 ─> 1 ─> 2 ─> 3 ─> 7 ─> 6 ─> 5 ─> 4 ─> None
>>> s_list.reverse(end_index=1)
>>> print(s_list)
1 ─> 0 ─> 2 ─> 3 ─> 7 ─> 6 ─> 5 ─> 4 ─> None
```

## LRU Cache

```
>>> from ezcode.list.lru_cache import LRUCache
>>> cache = LRUCache(capacity=3)
>>> cache.put(key=1, value="One")
>>> cache.put(key=2, value="Two")
>>> cache.put(key=3, value="Three")
>>> print(cache.get(1))
One
>>> cache.put(key=4, value="Four")
>>> print(cache.get(2))
None
```

## Monotonic Queue

### Monotonic Increasing Queue
```
>>> from ezcode.list.queue import MonotonicQueue
>>> mq = MonotonicQueue()
>>> for number in [5, 3, 1, 2, 4]:
...     mq.push(number)
...     print(mq)
... 
5
3
1
1 <─ 2
1 <─ 2 <─ 4
```
### Monotonic Decreasing Queue
```
>>> from ezcode.list.queue import MonotonicQueue
>>> mq = MonotonicQueue(is_increasing=False)
>>> for number in [5, 3, 1, 2, 4]:
...     mq.push(number)
...     print(mq)
... 
5
5 <─ 3
5 <─ 3 <─ 1
5 <─ 3 <─ 2
5 <─ 4
```