from ezcode.heap import PriorityQueue, PriorityMap, PriorityQueueOnPartialArray


def test_priority_queue():
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
        min_queue.push(push_data)
        assert min_queue.top(with_priority=True) == top_data
    for pop_data in ["A", "B", "C", "D", "E"]:
        assert min_queue.pop() == pop_data
    min_queue = PriorityQueue(["D", "C", "E", "A", "B"], key=lambda x: ord(x) - ord("A") + 1)
    for pop_data in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
        assert min_queue.pop(with_priority=True) == pop_data
    min_queue = PriorityQueue([("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)])
    assert min_queue.heap == [("A", 1), ("B", 2), ("E", 5), ("D", 4), ("C", 3)] 
    min_queue.update_top(("F", 6))
    assert min_queue.heap == [("B", 2), ("C", 3), ("E", 5), ("D", 4), ("F", 6)]
    min_queue.update_top(("B", 4))
    assert min_queue.heap == [("C", 3), ("B", 4), ("E", 5), ("D", 4), ("F", 6)]
    min_queue.update_top(("C", 2))
    assert min_queue.heap == [("C", 2), ("B", 4), ("E", 5), ("D", 4), ("F", 6)] 
    assert min_queue.top(len(min_queue)) == ["C", "B", "D", "E", "F"]
    push_list = [("D", 4), ("C", 3), ("E", 5), ("A", 1), ("B", 2)]
    max_top_list = [("D", 4), ("D", 4), ("E", 5), ("E", 5), ("E", 5)]
    max_queue = PriorityQueue(min_heap=False, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(push_list, max_top_list):
        max_queue.push(push_data)
        assert max_queue.top(with_priority=True) == top_data
    max_queue.update_top("E", 2)
    assert max_queue.heap == [("D", 4), ("C", 3), ("E", 2), ("A", 1), ("B", 2)]
    for pop_data in ["D", "C", "B", "E", "A"]:
        assert max_queue.pop() == pop_data
    max_queue = PriorityQueue(["D", "C", "E", "A", "B"], min_heap=False, key=lambda x: ord(x) - ord("A") + 1)
    for pop_data in [("E", 5), ("D", 4), ("C", 3), ("B", 2), ("A", 1)]:
        assert max_queue.pop(with_priority=True) == pop_data


def test_priority_map():
    min_map = PriorityMap(key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], [("D", 4), ("C", 3), ("C", 3), ("A", 1), ("A", 1)]):
        min_map.push(push_data)
        assert min_map.top(with_priority=True) == top_data
    for item, priority in zip(["A", "B", "C", "D", "E"], [1, 2, 3, 4, 5]):
        assert min_map[item] == priority
    min_map.update("C", 0)
    assert min_map.top() == "C"
    assert min_map["C"] == 0
    min_map["E"] = 3
    assert min_map.top(with_priority=True) == ("C", 0)
    assert min_map["E"] == 3
    assert min_map.top(len(min_map), with_priority=True) == [("C", 0), ("A", 1), ("B", 2), ("E", 3), ("D", 4)]
    min_map = PriorityMap({"D": 4, "C": 3, "E": 5, "A": 1, "B": 2})
    del min_map["D"]
    del min_map["B"]
    assert min_map.pop(len(min_map)) == ["A", "C", "E"]
    max_map = PriorityMap(min_heap=False, key=lambda x: ord(x) - ord("A") + 1)
    for push_data, top_data in zip(["D", "C", "E", "A", "B"], ["D", "D", "E", "E", "E"]):
        max_map.push(push_data)
        assert max_map.top() == top_data
    for item, priority in zip(["A", "B", "C", "D", "E"], [1, 2, 3, 4, 5]):
        assert max_map[item] == priority
    max_map["C"] = 0
    assert max_map.top(with_priority=True) == ("E", 5)
    assert max_map["C"] == 0
    max_map.push(item="B", priority=6)
    assert max_map.top() == "B"
    assert max_map["B"] == 6
    assert max_map.pop(3, with_priority=True) == [("B", 6), ("E", 5), ("D", 4)]
    max_map = PriorityMap({"D": 4, "C": 3, "E": 5, "A": 1, "B": 2}, min_heap=False)
    del max_map["E"]
    assert max_map.top(with_priority=True) == ("D", 4)
    del max_map["B"]
    assert max_map.top(len(max_map), with_priority=True) == [("D", 4), ("C", 3), ("A", 1)]
    del max_map["A"]
    assert max_map.top() == "D"
    del max_map["D"]
    assert max_map.top() == "C"
    del max_map["C"]
    assert len(max_map) == 0


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

    init_list = [("A", Priority(2, 2, 3)), ("B", Priority(2, 1, 1)), ("E", Priority(1, 1, 1)), ("D", Priority(1, 1, 2)), ("C", Priority(1, 1, 1))]
    min_queue = PriorityQueue(init_list)
    init_map = {"A": Priority(2, 2, 3), "B": Priority(2, 1, 1), "E": Priority(1, 1, 1), "D": Priority(1, 1, 2), "C": Priority(1, 1, 1)}
    min_map = PriorityMap(init_map) 
    for pop_data in [("E", Priority(1, 1, 1)), ("C", Priority(1, 1, 1)), ("D", Priority(1, 1, 2)), ("B", Priority(2, 1, 1)), ("A", Priority(2, 2, 3))]:
        assert min_queue.pop(with_priority=True) == pop_data
        assert min_map.pop(with_priority=True) == pop_data

    init_list = [[Priority(2, 2, 3), "A"], [Priority(2, 1, 1), "B"], [Priority(1, 1, 1), "E"], [Priority(1, 1, 2), "D"], [Priority(1, 1, 1), "C"]]
    max_queue = PriorityQueue(init_list, min_heap=False, key=lambda x: x[0])
    init_map = {"A": Priority(2, 2, 3), "B": Priority(2, 1, 1), "E": Priority(1, 1, 1), "D": Priority(1, 1, 2), "C": Priority(1, 1, 1)}
    max_map = PriorityMap(init_map, min_heap=False, key=lambda x: x[0])
    for pop_data in [[Priority(2, 2, 3), "A"], [Priority(2, 1, 1), "B"], [Priority(1, 1, 2), "D"], [Priority(1, 1, 1), "E"], [Priority(1, 1, 1), "C"]]:
        assert max_queue.pop() == pop_data
        assert max_map.pop(with_priority=True) == (pop_data[1], pop_data[0])


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





