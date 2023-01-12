from ezcode.Indexed.Array.rmq import SparseTable
from ezcode.Indexed.Array.search import binary_search, binary_search_range
from ezcode.Indexed.Array.sort import quick_sort
from ezcode.Indexed.Array.subarray import subarrays_with_target_sum
from ezcode.Indexed.Array.utils import copy, array_to_string, delete_all, rotate
from ezcode.Indexed.Array.utils import split_list, split_list_generator, chunk_list, chunk_list_generator
from ezcode.Indexed.Array.lcs import longest_common_subsequence, longest_common_subarray


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
    assert 0 == binary_search(target=0, array=[0])
    assert 0 == binary_search(target=0, array=[0, 1])
    assert 1 == binary_search(target=1, array=[0, 1])
    assert 0 == binary_search(target=0, array=[0, 1, 2])
    assert 1 == binary_search(target=1, array=[0, 1, 2])
    assert 2 == binary_search(target=2, array=[0, 1, 2])
    array, target = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 7
    assert binary_search(target=0, array=[]) is None
    assert binary_search(target=-1, array=array) is None
    assert 7 == binary_search(target=target, array=array, is_ascending=True)
    assert 2 == binary_search(target=target, array=array[::-1], is_ascending=False)
    assert (7, 7) == binary_search_range(target=target, array=array, is_ascending=True, is_inclusive=True)
    assert (None, None) == binary_search_range(target=3.5, array=array, is_ascending=True, is_inclusive=True)
    assert (3, 4) == binary_search_range(target=3.5, array=array, is_ascending=True, is_inclusive=False)
    assert (9, None) == binary_search_range(target=10, array=array, is_ascending=True, is_inclusive=False)
    assert (None, 0) == binary_search_range(target=-1, array=array, is_ascending=True, is_inclusive=False)
    assert (2, 2) == binary_search_range(target=target, array=array[::-1], is_ascending=False, is_inclusive=True)
    assert (None, None) == binary_search_range(target=3.5, array=array[::-1], is_ascending=False, is_inclusive=True)
    assert (5, 6) == binary_search_range(target=3.5, array=array[::-1], is_ascending=False, is_inclusive=False)
    assert (None, 0) == binary_search_range(target=10, array=array[::-1], is_ascending=False, is_inclusive=False)
    assert (9, None) == binary_search_range(target=-1, array=array[::-1], is_ascending=False, is_inclusive=False)
    array, target = [0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 7, 8, 9, 9], 3
    assert 4 == binary_search(target=target, array=array, is_ascending=True, has_duplicates=True, is_left_most=True)
    assert 7 == binary_search(target=target, array=array, is_ascending=True, has_duplicates=True, is_left_most=False)
    assert 9 == binary_search(target=target, array=array[::-1], is_ascending=False, has_duplicates=True, is_left_most=True)
    assert 12 == binary_search(target=target, array=array[::-1], is_ascending=False, has_duplicates=True, is_left_most=False)
    assert (4, 7) == binary_search_range(target=target, array=array, is_ascending=True, is_inclusive=True)
    assert (None, None) == binary_search_range(target=3.5, array=array, is_ascending=True, is_inclusive=True)
    assert (7, 8) == binary_search_range(target=3.5, array=array, is_ascending=True, is_inclusive=False)
    assert (16, None) == binary_search_range(target=10, array=array, is_ascending=True, is_inclusive=False)
    assert (None, 0) == binary_search_range(target=-1, array=array, is_ascending=True, is_inclusive=False)
    assert (9, 12) == binary_search_range(target=target, array=array[::-1], is_ascending=False, is_inclusive=True)
    assert (None, None) == binary_search_range(target=3.5, array=array[::-1], is_ascending=False, is_inclusive=True)
    assert (8, 9) == binary_search_range(target=3.5, array=array[::-1], is_ascending=False, is_inclusive=False)
    assert (None, 0) == binary_search_range(target=10, array=array[::-1], is_ascending=False, is_inclusive=False)
    assert (16, None) == binary_search_range(target=-1, array=array[::-1], is_ascending=False, is_inclusive=False)

    class P:
        def __init__(self, x, y):
            self.x, self.y = x, y

    assert 2 == binary_search(array=[(0, "zero"), (1, "one"), (2, "two")], target=2, key=lambda x: x[0])
    assert (1, 2) == binary_search_range(target=1, array=[P(0, 1), P(1, 1), P(1, 2), P(2, 2)], is_ascending=True, is_inclusive=True, key=lambda p: p.x)
    assert (2, 3) == binary_search_range(target=2, array=[P(0, 1), P(1, 1), P(1, 2), P(2, 2)], is_ascending=True, is_inclusive=True, key=lambda p: p.y)
    assert (0, 3) == binary_search_range(target=1, array=[P(0, 1), P(1, 1), P(1, 2), P(2, 2)], is_ascending=True, is_inclusive=False, key=lambda p: p.x)
    assert (1, None) == binary_search_range(target=2, array=[P(0, 1), P(1, 1), P(1, 2), P(2, 2)], is_ascending=True, is_inclusive=False, key=lambda p: p.y)


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


def test_copy():
    assert None == copy(None)
    assert [] == copy([])
    assert [[]] == copy([[]])
    assert [[], [1]] == copy([[], [1]])
    assert [[], [1, 2], 3] == copy([[], [1, 2], 3])
    assert [] != copy(None)
    assert [] != copy([[]])
    assert [1] != copy([[1]])
    assert [[], [1, 2]] != copy([[], [1, 3]])


def test_delete():
    array = [1, 2, 2, 2, 3, 4, 4, 5, 6]
    delete_all(array, set([2, 4, 6]))
    assert array == [1, 3, 5]


def test_longest_common_subsequence():
    assert "BCBA" == "".join(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))


def test_longest_common_subarray():
    assert "AB" == "".join(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))


def test_split_chunk_list():
    array = [1, 2, 3, 4, 5]
    split_benchmark = [
        [
            [1, 2, 3, 4, 5]
        ],
        [
            [1, 2, 3],
            [4, 5]
        ],
        [
            [1, 2],
            [3, 4],
            [5]
        ],
        [
            [1, 2],
            [3],
            [4],
            [5]
        ],
        [
            [1],
            [2],
            [3],
            [4],
            [5]
        ]
    ]
    for i in array:
        split_list(array, i) == split_benchmark[i - 1]
    split_list(array, 6) == split_benchmark[4]
    for i in array:
        sub_i = 0
        for sublist in split_list_generator(array, i):
            sublist == split_benchmark[i - 1][sub_i]
            sub_i += 1
    chunk_benchmark = [
        [
            [1],
            [2],
            [3],
            [4],
            [5]
        ],
        [
            [1, 2],
            [3, 4],
            [5]
        ],
        [
            [1, 2, 3],
            [4, 5]
        ],
        [
            [1, 2, 3, 4],
            [5]
        ],
        [
            [1, 2, 3, 4, 5]
        ]
    ]
    for i in array:
        chunk_list(array, i) == chunk_benchmark[i - 1]
    chunk_list(array, 6) == chunk_benchmark[4]
    for i in array:
        sub_i = 0
        for sublist in chunk_list_generator(array, i):
            sublist == chunk_benchmark[i - 1][sub_i]
            sub_i += 1


def test_quick_sort():
    data_1 = [7, 2, 4, 6, 5, 4, 1, 3, 8, 0, 6, 9, 4]
    data_2 = data_1.copy()
    quick_sort(data_1, reverse=False)
    quick_sort(data_2, reverse=True)
    assert data_1 == [0, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 9]
    assert data_2 == [9, 8, 7, 6, 6, 5, 4, 4, 4, 3, 2, 1, 0]


def test_rmq():
    st = SparseTable(merge=max, data_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert st.rmq(6, 9) == 9
    assert st.rmq(2, 6) == 6
    assert st.rmq(2, 8) == 8
    st = SparseTable(merge=min)
    st.build_table(data_list=[3, 2, 4, 5, 6, 8, 1, 9, 7, 0])
    assert st.rmq(0, 3) == 2
    assert st.rmq(2, 8) == 1
    assert st.rmq(3, 7) == 1
    assert st.rmq(4, 7) == 1
    assert st.rmq(7, 9) == 0
    assert st.rmq(7, 8) == 7
    assert st.rmq(0, 9) == 0
    assert st.rmq(2, 4) == 4


def test_subarrays_with_target_sum():
    array = [3, 5, -1, 2, 6, 3, -4, 5, 7, 9, -2, -3, 6]
    assert subarrays_with_target_sum(array, 3) == [(0, 0), (5, 5), (11, 12)]
    assert subarrays_with_target_sum(array, 6) == [(1, 3), (4, 4), (2, 6), (12, 12)]
    assert subarrays_with_target_sum(array, 11) == [(3, 5), (1, 6), (2, 7), (5, 8), (8, 11)]
    assert subarrays_with_target_sum(array, 12) == [(1, 4), (3, 7), (7, 8), (6, 11)]
    assert subarrays_with_target_sum(array, 13) == []
    assert subarrays_with_target_sum(array, 15) == [(0, 4), (1, 5), (6, 10), (5, 11)]
    assert subarrays_with_target_sum(array, 17) == [(4, 8), (6, 9), (8, 12)]
    assert subarrays_with_target_sum(array, 20) == [(5, 9)]
    assert subarrays_with_target_sum(array, 27) == [(2, 9), (1, 11), (4, 12)]













