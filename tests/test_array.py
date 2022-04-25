from ezcode.array.search import binary_search, binary_search_range
from ezcode.array.sort import quick_sort
from ezcode.array.utils import copy, array_to_string, delete_all, rotate
from ezcode.array.utils import split_list, split_list_generator, chunk_list, chunk_list_generator
from ezcode.array.lcs import longest_common_subsequence, longest_common_subarray
from fixture.utils import equal_list


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
    assert binary_search(array=[], target=0) is None
    assert binary_search(array=array, target=-1) is None
    assert 7 == binary_search(array=array, target=target, is_ascending=True)
    assert 2 == binary_search(array=array[::-1], target=target, is_ascending=False)
    assert (7, 7) == binary_search_range(array=array, target=target, is_ascending=True, is_inclusive=True)
    assert (None, None) == binary_search_range(array=array, target=3.5, is_ascending=True, is_inclusive=True)
    assert (3, 4) == binary_search_range(array=array, target=3.5, is_ascending=True, is_inclusive=False)
    assert (9, None) == binary_search_range(array=array, target=10, is_ascending=True, is_inclusive=False)
    assert (None, 0) == binary_search_range(array=array, target=-1, is_ascending=True, is_inclusive=False)
    assert (2, 2) == binary_search_range(array=array[::-1], target=target, is_ascending=False, is_inclusive=True)
    assert (None, None) == binary_search_range(array=array[::-1], target=3.5, is_ascending=False, is_inclusive=True)
    assert (5, 6) == binary_search_range(array=array[::-1], target=3.5, is_ascending=False, is_inclusive=False)
    assert (None, 0) == binary_search_range(array=array[::-1], target=10, is_ascending=False, is_inclusive=False)
    assert (9, None) == binary_search_range(array=array[::-1], target=-1, is_ascending=False, is_inclusive=False)
    array, target = [0, 1, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 7, 7, 8, 9, 9], 3
    assert 4 == binary_search(array=array, target=target, is_ascending=True, has_duplicates=True, is_left_most=True)
    assert 7 == binary_search(array=array, target=target, is_ascending=True, has_duplicates=True, is_left_most=False)
    assert 9 == binary_search(array=array[::-1], target=target, is_ascending=False, has_duplicates=True, is_left_most=True)
    assert 12 == binary_search(array=array[::-1], target=target, is_ascending=False, has_duplicates=True, is_left_most=False)
    assert (4, 7) == binary_search_range(array=array, target=target, is_ascending=True, is_inclusive=True)
    assert (None, None) == binary_search_range(array=array, target=3.5, is_ascending=True, is_inclusive=True)
    assert (7, 8) == binary_search_range(array=array, target=3.5, is_ascending=True, is_inclusive=False)
    assert (16, None) == binary_search_range(array=array, target=10, is_ascending=True, is_inclusive=False)
    assert (None, 0) == binary_search_range(array=array, target=-1, is_ascending=True, is_inclusive=False)
    assert (9, 12) == binary_search_range(array=array[::-1], target=target, is_ascending=False, is_inclusive=True)
    assert (None, None) == binary_search_range(array=array[::-1], target=3.5, is_ascending=False, is_inclusive=True)
    assert (8, 9) == binary_search_range(array=array[::-1], target=3.5, is_ascending=False, is_inclusive=False)
    assert (None, 0) == binary_search_range(array=array[::-1], target=10, is_ascending=False, is_inclusive=False)
    assert (16, None) == binary_search_range(array=array[::-1], target=-1, is_ascending=False, is_inclusive=False)


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


def test_equal_list():
    assert equal_list(None, None)
    assert equal_list([], [])
    assert equal_list([[]], [[]])
    assert equal_list([[], [1]], [[], [1]])
    assert equal_list([[], [1, 2], 3], [[], [1, 2], 3])
    assert not equal_list([], None)
    assert not equal_list([], [[]])
    assert not equal_list([1], [[1]])
    assert not equal_list([[], [1, 2]], [[], [1, 3]])


def test_copy():
    assert equal_list(None, copy(None))
    assert equal_list([], copy([]))
    assert equal_list([[]], copy([[]]))
    assert equal_list([[], [1]], copy([[], [1]]))
    assert equal_list([[], [1, 2], 3], copy([[], [1, 2], 3]))
    assert not equal_list([], copy(None))
    assert not equal_list([], copy([[]]))
    assert not equal_list([1], copy([[1]]))
    assert not equal_list([[], [1, 2]], copy([[], [1, 3]]))


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
        equal_list(split_list(array, i), split_benchmark[i - 1])
    equal_list(split_list(array, 6), split_benchmark[4])
    for i in array:
        sub_i = 0
        for sublist in split_list_generator(array, i):
            equal_list(sublist, split_benchmark[i - 1][sub_i])
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
        equal_list(chunk_list(array, i), chunk_benchmark[i - 1])
    equal_list(chunk_list(array, 6), chunk_benchmark[4])
    for i in array:
        sub_i = 0
        for sublist in chunk_list_generator(array, i):
            equal_list(sublist, chunk_benchmark[i - 1][sub_i])
            sub_i += 1


def test_quick_sort():
    data  = [7, 2, 4, 6, 5, 4, 1, 3, 8, 0, 6, 9, 4]
    quick_sort(data)
    assert data == [0, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 9]
















