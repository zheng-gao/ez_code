from random import randrange
from ezcode.Heap.PriorityMap import PriorityMap


def test_priority_map_top():
    size = 500
    random_list = [randrange(size) for _ in range(size)]
    pm = PriorityMap(random_list)
    assert pm.top(len(pm)) == sorted(random_list)
    pm = PriorityMap(random_list, reverse=True)
    assert pm.top(len(pm)) == sorted(random_list, reverse=True)


def test_priority_map_push_pop():
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
    max_map = PriorityMap(reverse=True, key=lambda x: ord(x) - ord("A") + 1)
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
    max_map = PriorityMap({"D": 4, "C": 3, "E": 5, "A": 1, "B": 2}, reverse=True)
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


def test_priority_queue_custom_comparator():

    class Priority:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        def check_type(self, other):
            if not isinstance(other, type(self)):
                raise NotImplementedError(f"{other} is not type {type(self)}")

        def __repr__(self):
            return f"({self.a},{self.b},{self.c})"

        def __eq__(self, other) -> bool:
            self.check_type(other)
            return self.a == other.a and self.b == other.b and self.c == other.c

        def __gt__(self, other) -> bool:
            self.check_type(other)
            return other.__lt__(self)

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
            return self.c < other.c

    init_map = {"A": Priority(2, 2, 3), "B": Priority(2, 1, 1), "E": Priority(1, 1, 1), "D": Priority(1, 1, 2), "C": Priority(1, 1, 1)}
    min_map = PriorityMap(init_map) 
    for pop_data in [("C", Priority(1, 1, 1)), ("E", Priority(1, 1, 1)), ("D", Priority(1, 1, 2)), ("B", Priority(2, 1, 1)), ("A", Priority(2, 2, 3))]:
        assert min_map.pop(with_priority=True) == pop_data

    init_map = {"A": Priority(2, 2, 3), "B": Priority(2, 1, 1), "E": Priority(1, 1, 1), "D": Priority(1, 1, 2), "C": Priority(1, 1, 1)}
    max_map = PriorityMap(init_map, reverse=True)
    for pop_data in [[Priority(2, 2, 3), "A"], [Priority(2, 1, 1), "B"], [Priority(1, 1, 2), "D"], [Priority(1, 1, 1), "E"], [Priority(1, 1, 1), "C"]]:
        assert max_map.pop(with_priority=True) == (pop_data[1], pop_data[0])

