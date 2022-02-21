from ezcode.array.heap import PriorityQueue, PriorityMap
from ezcode.array.search import binary_search
from ezcode.array.rotate import rotate
from ezcode.array.utils import copy, array_to_string, delete
from ezcode.array.lcs import longest_common_subsequence, longest_common_subarray
from fixture.utils import check_list_copy


def test_array_to_string():
    benchmark = """
[
    0,
    [1],
    [
        1,
        2,
        [0, 1, 2, 3],
    ],
    [],
    [
        [
            [0, 1, 2],
            0,
        ],
        1,
        2,
    ],
]
"""[1:]
    assert benchmark == array_to_string([0, [1], [1, 2, [0, 1, 2, 3]], [], [[[0, 1, 2], 0], 1, 2]])


def test_binary_search():
    assert 0 == binary_search(array=[0], target=0)
    assert 0 == binary_search(array=[0, 1], target=0)
    assert 1 == binary_search(array=[0, 1], target=1)
    assert 0 == binary_search(array=[0, 1, 2], target=0)
    assert 1 == binary_search(array=[0, 1, 2], target=1)
    assert 2 == binary_search(array=[0, 1, 2], target=2)
    array, target = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 7
    assert None == binary_search(array=[], target=0)
    assert None == binary_search(array=array, target=-1)
    assert 7 == binary_search(array=array, target=target, is_ascending=True)
    assert 2 == binary_search(array=array[::-1], target=target, is_ascending=False)
    array, target = [0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 7, 8, 9, 9], 3
    assert 4 == binary_search(array=array, target=target, is_ascending=True, is_left_most=True)
    assert 7 == binary_search(array=array, target=target, is_ascending=True, is_left_most=False)
    assert 9 == binary_search(array=array[::-1], target=target, is_ascending=False, is_left_most=True)
    assert 12 == binary_search(array=array[::-1], target=target, is_ascending=False, is_left_most=False)


def test_rotate():
    array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    array_left_rotated = array.copy()
    rotate(array_left_rotated, 3, is_left_rotate=True)
    for a, b in zip([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], array_left_rotated):
        assert a == b
    array_right_rotated = array.copy()
    rotate(array_right_rotated, 4, is_left_rotate=False)
    for a, b in zip([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], array_right_rotated):
        assert a == b


def test_check_list_copy():
    assert check_list_copy(None, None)
    assert check_list_copy([], [])
    assert check_list_copy([[]], [[]])
    assert check_list_copy([[],[1]], [[],[1]])
    assert check_list_copy([[],[1, 2], 3], [[],[1, 2], 3])
    assert not check_list_copy([], None)
    assert not check_list_copy([], [[]])
    assert not check_list_copy([1], [[1]])
    assert not check_list_copy([[],[1, 2]], [[],[1, 3]])


def test_copy():
    assert check_list_copy(None, copy(None))
    assert check_list_copy([], copy([]))
    assert check_list_copy([[]], copy([[]]))
    assert check_list_copy([[],[1]], copy([[],[1]]))
    assert check_list_copy([[],[1, 2], 3], copy([[],[1, 2],3]))
    assert not check_list_copy([], copy(None))
    assert not check_list_copy([], copy([[]]))
    assert not check_list_copy([1], copy([[1]]))
    assert not check_list_copy([[],[1, 2]], copy([[],[1, 3]]))


def test_delete():
    array = [1, 2, 2, 2, 3, 4, 4, 5, 6]
    delete(array, set([2, 4, 6]))
    assert check_list_copy([1, 3, 5], array)


def test_longest_common_subsequence():
    assert "BCBA" == "".join(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))


def test_longest_common_subarray():
    assert "AB" == "".join(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))


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



    
