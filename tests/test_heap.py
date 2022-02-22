from ezcode.heap import PriorityQueue, PriorityMap


def test_priority_queue():
    push_list = [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]

    min_pq = PriorityQueue()
    min_peek_list = [(4, "D"), (3, "C"), (3, "C"), (1, "A"), (1, "A")]
    for push_data, peek_data in zip(push_list, min_peek_list):
        min_pq.push(push_data)
        assert min_pq.peek() == peek_data
    min_pop_list = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E")]
    for pop_data in min_pop_list:
        assert min_pq.pop() == pop_data
    min_pq = PriorityQueue(push_list)
    for pop_data in min_pop_list:
        assert min_pq.pop() == pop_data

    max_pq = PriorityQueue(min_heap=False)
    max_peek_list = [(4, "D"), (4, "D"), (5, "E"), (5, "E"), (5, "E")]
    for push_data, peek_data in zip(push_list, max_peek_list):
        max_pq.push(push_data)
        assert max_pq.peek() == peek_data
    max_pop_list = [(5, "E"), (4, "D"), (3, "C"), (2, "B"), (1, "A")]
    for pop_data in max_pop_list:
        assert max_pq.pop() == pop_data
    max_pq = PriorityQueue(push_list, min_heap=False)
    for pop_data in max_pop_list:
        assert max_pq.pop() == pop_data


def test_priority_map():
    push_list = [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]

    min_map = PriorityMap()
    min_peek_list = [(4, "D"), (3, "C"), (3, "C"), (1, "A"), (1, "A")]
    for push_data, peek_data in zip(push_list, min_peek_list):
        min_map.push(push_data)
        assert min_map.peek() == peek_data
    for key, priority in zip(["A", "B", "C", "D", "E"], [1, 2, 3, 4, 5]):
        assert min_map.get_priority(key) == priority
    min_map.update(0, "C")
    assert min_map.peek() == (0, "C")
    assert min_map.get_priority("C") == 0
    min_map.update(3, "E")
    assert min_map.peek() == (0, "C")
    assert min_map.get_priority("E") == 3
    min_pop_list = [(0, "C"), (1, "A"), (2, "B"), (3, "E"), (4, "D")]
    for pop_data in min_pop_list:
        assert min_map.pop() == pop_data
    min_map = PriorityMap({"D": 4, "C": 3, "E": 5, "A": 1, "B": 2})
    min_map.delete("D")
    min_map.delete("B")
    min_pop_list = [(1, "A"), (3, "C"), (5, "E")]
    for pop_data in min_pop_list:
        assert min_map.pop() == pop_data


    max_map = PriorityMap(min_heap=False)
    max_peek_list = [(4, "D"), (4, "D"), (5, "E"), (5, "E"), (5, "E")]
    for push_data, peek_data in zip(push_list, max_peek_list):
        max_map.push(push_data)
        assert max_map.peek() == peek_data
    for key, priority in zip(["A", "B", "C", "D", "E"], [1, 2, 3, 4, 5]):
        assert max_map.get_priority(key) == priority
    max_map.update(0, "C")
    assert max_map.peek() == (5, "E")
    assert max_map.get_priority("C") == 0
    max_map.update(6, "B")
    assert max_map.peek() == (6, "B")
    assert max_map.get_priority("B") == 6
    max_pop_list = [(6, "B"), (5, "E"), (4, "D"), (1, "A"), (0, "C")]
    for pop_data in max_pop_list:
        assert max_map.pop() == pop_data
    max_map = PriorityMap({"D": 4, "C": 3, "E": 5, "A": 1, "B": 2}, min_heap=False)
    max_map.delete("D")
    max_map.delete("B")
    max_pop_list = [(5, "E"), (3, "C"), (1, "A")]
    for pop_data in max_pop_list:
        assert max_map.pop() == pop_data
