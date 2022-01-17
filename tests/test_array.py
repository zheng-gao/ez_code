from ezcode.array.search import binary_search
from ezcode.array.rotate import rotate
from ezcode.array.utils import is_copied, copy, array_to_string, delete


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


def test_is_copied():
    assert is_copied(None, None)
    assert is_copied([], [])
    assert is_copied([[]], [[]])
    assert is_copied([[],[1]], [[],[1]])
    assert is_copied([[],[1, 2], 3], [[],[1, 2], 3])
    assert not is_copied([], None)
    assert not is_copied([], [[]])
    assert not is_copied([1], [[1]])
    assert not is_copied([[],[1, 2]], [[],[1, 3]])


def test_copy():
    assert is_copied(None, copy(None))
    assert is_copied([], copy([]))
    assert is_copied([[]], copy([[]]))
    assert is_copied([[],[1]], copy([[],[1]]))
    assert is_copied([[],[1, 2], 3], copy([[],[1, 2],3]))
    assert not is_copied([], copy(None))
    assert not is_copied([], copy([[]]))
    assert not is_copied([1], copy([[1]]))
    assert not is_copied([[],[1, 2]], copy([[],[1, 3]]))


def test_delete():
    array = [1, 2, 2, 2, 3, 4, 4, 5, 6]
    delete(array, set([2, 4, 6]))
    assert is_copied([1, 3, 5], array)




