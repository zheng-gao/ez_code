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