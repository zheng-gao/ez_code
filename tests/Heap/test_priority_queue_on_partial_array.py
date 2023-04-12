from random import randrange
from ezcode.Heap.PriorityQueueOnPartialArray import PriorityQueueOnPartialArray


def test_priority_queue_on_partial_array_top():
    size = 500
    array = [0] * (size * 2)
    random_list = [randrange(size) for _ in range(size)]
    start = randrange(size)
    pm = PriorityQueueOnPartialArray(array=array, init_data=random_list, start=start)
    assert pm.top(len(pm)) == sorted(random_list)
    pm = PriorityQueueOnPartialArray(array=array, init_data=random_list, reverse=True, start=start)
    assert pm.top(len(pm)) == sorted(random_list, reverse=True)


def test_priority_queue_on_partial_array_push_pop():
    min_queue = PriorityQueueOnPartialArray(array=[None] * 9, start=3, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], [("D", 4), ("C", 3), ("C", 3), ("A", 1), ("A", 1)]):
        min_queue.push(push_data)
        assert min_queue.top(with_priority=True) == top_data
    assert min_queue.heap == [None, None, None, "A", "B", "E", "D", "C", None]
    assert min_queue.pop(len(min_queue), with_priority=True) == [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]

    max_queue = PriorityQueueOnPartialArray(array=[None] * 9, reverse=True, start=2, end=6, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], [("D", 4), ("D", 4), ("E", 5), ("E", 5), ("E", 5)]):
        max_queue.push(push_data)
        assert max_queue.top(with_priority=True) == top_data
    assert max_queue.heap == [None, None, "E", "C", "D", "A", "B", None, None]
    assert max_queue.pop(len(max_queue), with_priority=True) == [("E", 5), ("D", 4), ("C", 3), ("B", 2), ("A", 1)]

