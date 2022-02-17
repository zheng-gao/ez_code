from ezcode.heap.priority_queue import PriorityQueue


def test_priority_queue():
    min_q = PriorityQueue()
    for data, peek_data in zip([4, 3, 5, 1, 2], [4, 3, 3, 1, 1]):
        min_q.push(data)
        assert min_q.peek() == peek_data
    for pop_data in [1, 2, 3, 4, 5]:
        assert min_q.pop() == pop_data

    max_q = PriorityQueue(is_min=False)
    for data, peek_data in zip([4, 3, 5, 1, 2], [4, 4, 5, 5, 5]):
        max_q.push(data)
        assert max_q.peek() == peek_data
    for pop_data in [5, 4, 3, 2, 1]:
        assert max_q.pop() == pop_data
