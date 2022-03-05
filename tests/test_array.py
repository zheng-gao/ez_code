from ezcode.array.matrix import init_matrix, MatrixIterator
from ezcode.array.search import binary_search
from ezcode.array.rotate import rotate
from ezcode.array.utils import copy, array_to_string, delete
from ezcode.array.utils import split_list, split_list_generator, chunk_list, chunk_list_generator
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
    assert binary_search(array=[], target=0) is None
    assert binary_search(array=array, target=-1) is None
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
    assert check_list_copy([[], [1]], [[], [1]])
    assert check_list_copy([[], [1, 2], 3], [[], [1, 2], 3])
    assert not check_list_copy([], None)
    assert not check_list_copy([], [[]])
    assert not check_list_copy([1], [[1]])
    assert not check_list_copy([[], [1, 2]], [[], [1, 3]])


def test_copy():
    assert check_list_copy(None, copy(None))
    assert check_list_copy([], copy([]))
    assert check_list_copy([[]], copy([[]]))
    assert check_list_copy([[], [1]], copy([[], [1]]))
    assert check_list_copy([[], [1, 2], 3], copy([[], [1, 2], 3]))
    assert not check_list_copy([], copy(None))
    assert not check_list_copy([], copy([[]]))
    assert not check_list_copy([1], copy([[1]]))
    assert not check_list_copy([[], [1, 2]], copy([[], [1, 3]]))


def test_delete():
    array = [1, 2, 2, 2, 3, 4, 4, 5, 6]
    delete(array, set([2, 4, 6]))
    assert check_list_copy([1, 3, 5], array)


def test_longest_common_subsequence():
    assert "BCBA" == "".join(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))


def test_longest_common_subarray():
    assert "AB" == "".join(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))


def test_init_matrix():
    class Data:
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return str(self.data)

    matrix = init_matrix(2, 3, Data(1))
    matrix[0][0].data = 2
    assert matrix[0][0].data == 2
    assert matrix[0][1].data == 1
    assert matrix[1][0].data == 1


def test_matrix_iterator():
    size = 4
    matrix = init_matrix(size, size)
    for row in range(size):
        for col in range(size):
            matrix[row][col] = size * row + col
    #  0  1  2  3
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15
    for row in range(size):
        iterator = MatrixIterator(matrix, row, 0, direction="horizontal")
        for col in range(size):
            assert matrix[row][col] == next(iterator)
    for col in range(size):
        iterator = MatrixIterator(matrix, 0, col, direction="vertical")
        for row in range(size):
            assert matrix[row][col] == next(iterator)
    for i in range(size):
        row_start = size - i - 1
        iterator = MatrixIterator(matrix, row_start, 0, direction="ascending-diagonal")
        for row, col in zip(range(row_start, -1, -1), range(0, i + 1)):
            assert matrix[row][col] == next(iterator)
    for i in range(size):
        iterator = MatrixIterator(matrix, 0, i, direction="descending-diagonal")
        for row, col in zip(range(0, size - i), range(i, size - i)):
            print(f"{row}, {col}")
            assert matrix[row][col] == next(iterator)


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
        check_list_copy(split_list(array, i), split_benchmark[i - 1])
    check_list_copy(split_list(array, 6), split_benchmark[4])
    for i in array:
        sub_i = 0
        for sublist in split_list_generator(array, i):
            check_list_copy(sublist, split_benchmark[i - 1][sub_i])
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
        check_list_copy(chunk_list(array, i), chunk_benchmark[i - 1])
    check_list_copy(chunk_list(array, 6), chunk_benchmark[4])
    for i in array:
        sub_i = 0
        for sublist in chunk_list_generator(array, i):
            check_list_copy(sublist, chunk_benchmark[i - 1][sub_i])
            sub_i += 1
