from ezcode.heap.priority_queue import PriorityQueue


def test_priority_queue():
    push_list = [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]

    min_q = PriorityQueue()
    min_peek_list = [(4, "D"), (3, "C"), (3, "C"), (1, "A"), (1, "A")]
    min_pop_list = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E")]
    for push_data, peek_data in zip(push_list, min_peek_list):
        min_q.push(push_data)
        assert min_q.peek() == peek_data
    for pop_data in min_pop_list:
        assert min_q.pop() == pop_data
    min_q = PriorityQueue(push_list)
    for pop_data in min_pop_list:
        assert min_q.pop() == pop_data

    max_q = PriorityQueue(min_heap=False)
    max_peek_list = [(4, "D"), (4, "D"), (5, "E"), (5, "E"), (5, "E")]
    max_pop_list = [(5, "E"), (4, "D"), (3, "C"), (2, "B"), (1, "A")]
    for push_data, peek_data in zip(push_list, max_peek_list):
        max_q.push(push_data)
        assert max_q.peek() == peek_data
    for pop_data in max_pop_list:
        assert max_q.pop() == pop_data
    max_q = PriorityQueue(push_list, min_heap=False)
    for pop_data in max_pop_list:
        assert max_q.pop() == pop_data
