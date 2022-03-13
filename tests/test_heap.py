from fixture.utils import equal_list
from ezcode.heap import PriorityQueue, PriorityMap


def test_priority_queue():
    min_queue = PriorityQueue([4, 3, 5, 1, 2])
    assert equal_list(min_queue.top_n(3), [1, 2, 3])
    assert equal_list(min_queue.top_n(), [1, 2, 3, 4, 5])
    for pop_data in [1, 2, 3, 4, 5]:
        assert min_queue.pop() == pop_data
    max_queue = PriorityQueue([4, 3, 5, 1, 2], min_heap=False)
    assert equal_list(max_queue.top_n(3), [5, 4, 3])
    assert equal_list(max_queue.top_n(), [5, 4, 3, 2, 1])
    for pop_data in [5, 4, 3, 2, 1]:
        assert max_queue.pop() == pop_data

    push_list = [(4, "D"), (3, "C"), (5, "E"), (1, "A"), (2, "B")]

    min_queue = PriorityQueue()
    min_peek_list = [(4, "D"), (3, "C"), (3, "C"), (1, "A"), (1, "A")]
    for push_data, peek_data in zip(push_list, min_peek_list):
        min_queue.push(push_data)
        assert min_queue.peek() == peek_data
    min_pop_list = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E")]
    for pop_data in min_pop_list:
        assert min_queue.pop() == pop_data
    min_queue = PriorityQueue(push_list)
    for pop_data in min_pop_list:
        assert min_queue.pop() == pop_data

    max_queue = PriorityQueue(min_heap=False)
    max_peek_list = [(4, "D"), (4, "D"), (5, "E"), (5, "E"), (5, "E")]
    for push_data, peek_data in zip(push_list, max_peek_list):
        max_queue.push(push_data)
        assert max_queue.peek() == peek_data
    max_pop_list = [(5, "E"), (4, "D"), (3, "C"), (2, "B"), (1, "A")]
    for pop_data in max_pop_list:
        assert max_queue.pop() == pop_data
    max_queue = PriorityQueue(push_list, min_heap=False)
    for pop_data in max_pop_list:
        assert max_queue.pop() == pop_data


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


def test_heap_custom_comparator():

    class Priority:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def check_type(self, other):
            if not isinstance(other, type(self)):
                raise NotImplementedError(f"{other} is not type {type(self)}")

        def __str__(self):
            return f"({self.a},{self.b},{self.c})"

        def __eq__(self, other) -> bool:
            self.check_type(other)
            return not self < other and not other < self

        def __gt__(self, other) -> bool:
            self.check_type(other)
            return other < self

        def __lt__(self, other) -> bool:
            self.check_type(other)
            if self.a < other.a:
                return True
            if other.a < self.a:
                return False
            if self.b < other.b:
                return True
            if other.b < self.b:
                return False
            return self.c < self.c

    push_list = [(Priority(2, 2, 3), "A"), (Priority(2, 1, 1), "B"), (Priority(1, 1, 1), "E"), (Priority(1, 1, 2), "D"), (Priority(1, 1, 1), "C")]

    min_queue = PriorityQueue(push_list)
    push_map = {"A": Priority(2, 2, 3), "B": Priority(2, 1, 1), "E": Priority(1, 1, 1), "D": Priority(1, 1, 2), "C": Priority(1, 1, 1)}
    min_map = PriorityMap(push_map)
    min_pop_list = [(Priority(1, 1, 1), "E"), (Priority(1, 1, 1), "C"), (Priority(1, 1, 2), "D"), (Priority(2, 1, 1), "B"), (Priority(2, 2, 3), "A")]
    for pop_data in min_pop_list:
        assert min_queue.pop() == pop_data
        assert min_map.pop() == pop_data

    max_queue = PriorityQueue(push_list, min_heap=False)
    max_pop_list = [(Priority(2, 2, 3), "A"), (Priority(2, 1, 1), "B"), (Priority(1, 1, 2), "D"), (Priority(1, 1, 1), "E"), (Priority(1, 1, 1), "C")]
    max_map = PriorityMap(min_heap=False)
    for push_data in push_list:
        max_map.push(push_data)
    for pop_data in max_pop_list:
        assert max_queue.pop() == pop_data
        assert max_map.pop() == pop_data
