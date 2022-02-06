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