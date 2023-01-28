from ezcode.Array.Utils import copy, delete_all, rotate
from ezcode.Array.Utils import split_list, split_list_generator, chunk_list, chunk_list_generator


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















