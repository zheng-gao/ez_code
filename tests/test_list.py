from ezcode.list.stack import Stack, MinStack, MaxStack
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
    assert lru_cache.get(1) is None
    lru_cache.put(key=1, value=1)
    lru_cache.put(key=2, value=2)
    lru_cache.put(key=3, value=3)
    assert lru_cache.get(1) == 1     # 1 3 2
    lru_cache.put(key=4, value=4)    # 4 1 3 (no 2)
    assert lru_cache.get(2) is None
    assert lru_cache.get(4) == 4     # 4 1 3
    lru_cache.put(key=3, value=33)   # 3 4 1
    lru_cache.put(key=5, value=5)    # 5 3 4 (no 1)
    assert lru_cache.get(1) is None
    assert lru_cache.get(3) == 33
    assert lru_cache.get(5) == 5


def test_min_max_stack():
    min_stack = MinStack()
    max_stack = MaxStack()
    for data, min_data, max_data in zip([2, 1, 3, 5, 4], [2, 1, 1, 1, 1], [2, 2, 3, 5, 5]):
        min_stack.push(data)
        max_stack.push(data)
        assert min_stack.get_min() == min_data
        assert max_stack.get_max() == max_data
    for min_data, max_data in zip([1, 1, 1, 2], [5, 3, 2, 2]):
        min_stack.pop()
        max_stack.pop()
        assert min_stack.get_min() == min_data
        assert max_stack.get_max() == max_data


def test_monontonic_queue():
    mq = MonotonicQueue(is_increasing=True)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 3, 1, 1, 1]):
        mq.push(data)
        assert mq.peek() == benchmark
    mq = MonotonicQueue(is_increasing=False)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 5, 5, 5, 5]):
        mq.push(data)
        assert mq.peek() == benchmark
