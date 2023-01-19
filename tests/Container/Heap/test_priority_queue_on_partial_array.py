from ezcode.Container.Heap.PriorityQueueOnPartialArray import PriorityQueueOnPartialArray


def test_priority_queue_on_partial_array():
    min_queue = PriorityQueueOnPartialArray(array=[None] * 9, min_heap=True, start=3, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], [("D", 4), ("C", 3), ("C", 3), ("A", 1), ("A", 1)]):
        min_queue.push(push_data)
        assert min_queue.top(with_priority=True) == top_data
    assert min_queue.heap == [None, None, None, "A", "B", "E", "D", "C", None]
    assert min_queue.pop(len(min_queue), with_priority=True) == [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]

    max_queue = PriorityQueueOnPartialArray(array=[None] * 9, min_heap=False, start=2, end=6, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], [("D", 4), ("D", 4), ("E", 5), ("E", 5), ("E", 5)]):
        max_queue.push(push_data)
        assert max_queue.top(with_priority=True) == top_data
    assert max_queue.heap == [None, None, "E", "C", "D", "A", "B", None, None]
    assert max_queue.pop(len(max_queue), with_priority=True) == [("E", 5), ("D", 4), ("C", 3), ("B", 2), ("A", 1)]

