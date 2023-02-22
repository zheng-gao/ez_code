from collections.abc import MutableMapping
from ezcode.Cache.LRUCache import LRUCache


def test_lru_cache_type():
    assert isinstance(LRUCache(), MutableMapping)


def test_lru_cache_iterator():
    c = LRUCache()
    for i in range(10):
        c[i] = i
    assert list(c) == sorted(range(10), reverse=True)
    assert list(c.keys(reverse=True)) == sorted(range(10))
    assert list(c.values(reverse=True)) == sorted(range(10))
    assert list(reversed(c)) == list(range(10))
    assert list(c.items(reverse=True)) == list(zip(range(10), range(10)))


def test_lru_cache_pop():
    c = LRUCache()
    for i in range(10):
        c[i] = i
    assert c.pop(3) == 3
    assert c.pop(8) == 8


def test_lru_cache_pop_item():
    c = LRUCache()
    for i in range(10):
        c[i] = i
    assert c.popitem() == (9, 9)
    assert c.popitem() == (8, 8)
    assert c.popitem(reverse=True) == (0, 0)
    assert c.popitem(reverse=True) == (1, 1)


def test_lru_cache():
    lru_cache = LRUCache(capacity=3)
    assert 1 not in lru_cache
    lru_cache[1] = 1
    lru_cache[2] = 2
    lru_cache[3] = 3          # 3 2 1
    assert lru_cache[1] == 1  # 1 3 2
    lru_cache[4] = 4          # 4 1 3 (no 2)
    assert 2 not in lru_cache
    assert lru_cache[4] == 4  # 4 1 3
    assert 1 in lru_cache
    lru_cache[3] = 33  # 3 4 1
    lru_cache[5] = 5   # 5 3 4 (no 1)
    assert 1 not in lru_cache
    assert lru_cache[3] == 33
    assert lru_cache[5] == 5

