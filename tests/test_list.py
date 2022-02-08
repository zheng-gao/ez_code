from ezcode.list.stack import Stack
from ezcode.list.queue import Queue, MonotonicQueue
from ezcode.list.lru_cache import LRUCache
from fixture.list import s_list, s_list_copied, s_list_reversed


def test_print():
    pass


def test_is_copied():
    assert s_list.is_copied(s_list_copied)


def test_copy():
    assert s_list.copy().is_copied(s_list_copied)
    assert not s_list.is_copied(s_list_reversed)


def test_reverse():
    reversed_list = s_list.copy()
    reversed_list.reverse()
    assert reversed_list.is_copied(s_list_reversed)


def test_queue():
    queue = Queue()
    for i in range(3):
        assert len(queue) == i
        queue.push(i)
        assert queue.peek() == 0
    for i in range(3):
        assert len(queue) == 3 - i
        assert queue.peek() == i
        assert queue.pop() == i


def test_stack():
    stack = Stack()
    for i in range(3):
        assert len(stack) == i
        stack.push(i)
        assert stack.peek() == i
    for i in range(3):
        assert len(stack) == 3 - i
        assert stack.peek() == 2 - i
        assert stack.pop() == 2 - i


def test_lru_cache():
    lru_cache = LRUCache(capacity=3)
    assert lru_cache.get(1) == None
    lru_cache.put(key=1, value=1)
    lru_cache.put(key=2, value=2)
    lru_cache.put(key=3, value=3)
    assert lru_cache.get(1) == 1     # 1 3 2
    lru_cache.put(key=4, value=4)    # 4 1 3 (no 2)
    assert lru_cache.get(2) == None  
    assert lru_cache.get(4) == 4     # 4 1 3
    lru_cache.put(key=3, value=33)   # 3 4 1
    lru_cache.put(key=5, value=5)    # 5 3 4 (no 1)
    assert lru_cache.get(1) == None
    assert lru_cache.get(3) == 33
    assert lru_cache.get(5) == 5


def test_monontic_queue():
    mq = MonotonicQueue(is_increasing=True)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 3, 1, 1, 1]):
        mq.push(data)
        assert mq.peek() == benchmark
    mq = MonotonicQueue(is_increasing=False)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 5, 5, 5, 5]):
        mq.push(data)
        assert mq.peek() == benchmark
