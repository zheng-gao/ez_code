from ezcode.Array.Search import binary_search, binary_search_range


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

