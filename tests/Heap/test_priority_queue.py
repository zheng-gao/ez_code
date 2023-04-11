from ezcode.Heap.PriorityQueue import PriorityQueue


def test_priority_queue_push_pop_top():
    min_queue = PriorityQueue([4, 3, 5, 1, 2])
    assert min_queue.top(3) == [1, 2, 3]
    assert min_queue.top(len(min_queue)) == [1, 2, 3, 4, 5]
    for pop_data in [1, 2, 3, 4, 5]:
        assert min_queue.pop() == pop_data
    max_queue = PriorityQueue([4, 3, 5, 1, 2], min_heap=False)
    assert max_queue.top(3) == [5, 4, 3]
    assert max_queue.top(len(max_queue)) == [5, 4, 3, 2, 1]
    for pop_data in [5, 4, 3, 2, 1]:
        assert max_queue.pop() == pop_data
    push_list = [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]
    min_top_list = [("D", 4), ("C", 3), ("C", 3), ("A", 1), ("A", 1)]
    min_queue = PriorityQueue()
    for push_data, top_data in zip(push_list, min_top_list):
        min_queue.push(*push_data)
        assert min_queue.top(with_priority=True) == top_data
    for pop_data in ["A", "B", "C", "D", "E"]:
        assert min_queue.pop() == pop_data
    min_queue = PriorityQueue(["D", "C", "E", "A", "B"], key=lambda x: ord(x) - ord("A") + 1)
    for pop_data in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
        assert min_queue.pop(with_priority=True) == pop_data
    min_queue = PriorityQueue([("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)])
    assert min_queue.heap == [("A", 1), ("B", 2), ("E", 5), ("D", 4), ("C", 3)] 
    min_queue.update_top("F", 6)
    assert min_queue.heap == [("B", 2), ("C", 3), ("E", 5), ("D", 4), ("F", 6)]
    min_queue.update_top("B", 4)
    assert min_queue.heap == [("C", 3), ("B", 4), ("E", 5), ("D", 4), ("F", 6)]
    min_queue.update_top("C", 2)
    assert min_queue.heap == [("C", 2), ("B", 4), ("E", 5), ("D", 4), ("F", 6)] 
    assert min_queue.top(len(min_queue)) == ["C", "B", "D", "E", "F"]
    push_list = [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]
    max_top_list = [("D", 4), ("D", 4), ("E", 5), ("E", 5), ("E", 5)]
    max_queue = PriorityQueue(min_heap=False, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(push_list, max_top_list):
        max_queue.push(*push_data)
        assert max_queue.top(with_priority=True) == top_data
    max_queue.update_top("E", 2)
    assert max_queue.heap == [("D", 4), ("C", 3), ("E", 2), ("A", 1), ("B", 2)]
    for pop_data in ["D", "C", "B", "E", "A"]:
        assert max_queue.pop() == pop_data
    max_queue = PriorityQueue(["D", "C", "E", "A", "B"], min_heap=False, key=lambda x: ord(x) - ord("A") + 1)
    for pop_data in [("E", 5), ("D", 4), ("C", 3), ("B", 2), ("A", 1)]:
        assert max_queue.pop(with_priority=True) == pop_data


def test_priority_queue_heapify():
    pq = PriorityQueue()
    pq.heapify([4, 3, 5, 1, 2], min_heap=True)
    pq.top(len(pq)) == [1, 2, 3, 4, 5]
    pq.heapify([4, 3, 5, 1, 2], min_heap=False)
    pq.top(len(pq)) == [5, 4, 3, 2, 1]
    pq.heapify([("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)], min_heap=True, key=lambda x: x[1], unpack_pairs=False)
    pq.top(len(pq)) == [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]
    pq.heapify([("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)], min_heap=True, unpack_pairs=True)
    pq.top(len(pq)) == ["A", "B", "C", "D", "E"]
    pq.top(len(pq), with_priority=True) == [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]


def test_priority_queue_custom_comparator():

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

    init_list = [("A", Priority(2, 2, 3)), ("B", Priority(2, 1, 1)), ("E", Priority(1, 1, 1)), ("D", Priority(1, 1, 2)), ("C", Priority(1, 1, 1))]
    min_queue = PriorityQueue(init_list) 
    for pop_data in [("E", Priority(1, 1, 1)), ("C", Priority(1, 1, 1)), ("D", Priority(1, 1, 2)), ("B", Priority(2, 1, 1)), ("A", Priority(2, 2, 3))]:
        assert min_queue.pop(with_priority=True) == pop_data

    init_list = [[Priority(2, 2, 3), "A"], [Priority(2, 1, 1), "B"], [Priority(1, 1, 1), "E"], [Priority(1, 1, 2), "D"], [Priority(1, 1, 1), "C"]]
    max_queue = PriorityQueue(init_list, min_heap=False, key=lambda x: x[0], unpack_pairs=False)
    for pop_data in [[Priority(2, 2, 3), "A"], [Priority(2, 1, 1), "B"], [Priority(1, 1, 2), "D"], [Priority(1, 1, 1), "E"], [Priority(1, 1, 1), "C"]]:
        assert max_queue.pop() == pop_data

