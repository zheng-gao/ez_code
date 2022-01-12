from ezcode.array.search import binary_search
from ezcode.array.rotate import rotate


def test_binary_search():
    array, target = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 7
    assert None == binary_search(array=[], target=-1)
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



