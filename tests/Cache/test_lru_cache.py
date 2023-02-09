# from ezcode.Cache.LRUCache import LRUCache
# 
# 
# def test_lru_cache():
#     lru_cache = LRUCache(capacity=3)
#     assert lru_cache.get(1) is None
#     lru_cache.put(key=1, value=1)
#     lru_cache.put(key=2, value=2)
#     lru_cache.put(key=3, value=3)
#     assert lru_cache.get(1) == 1     # 1 3 2
#     lru_cache.put(key=4, value=4)    # 4 1 3 (no 2)
#     assert lru_cache.get(2) is None
#     assert lru_cache.get(4) == 4     # 4 1 3
#     lru_cache.put(key=3, value=33)   # 3 4 1
#     lru_cache.put(key=5, value=5)    # 5 3 4 (no 1)
#     assert lru_cache.get(1) is None
#     assert lru_cache.get(3) == 33
#     assert lru_cache.get(5) == 5

