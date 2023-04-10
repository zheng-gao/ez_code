from ezcode.Array.Merge import merge_sorted_arrays


def test_merge_sorted_arrays():
    arrays = [
        [3, 11, 25, 33],
        [1, 15, 18, 42, 57],
        [],
        [12, 16, 28, 60],
        [7, 26, 40],
        [41, 50] 
    ]
    assert list(merge_sorted_arrays(arrays)) == [
        1, 3, 7, 11, 12, 15, 16, 18, 25, 26, 28, 33, 40, 41, 42, 50, 57, 60
    ]

    arrays = [
        [(0, 3), (1, 4), (5, 6)],
        [(1, 2), (3, 4)],
        [(4, 10)]
    ]
    assert list(merge_sorted_arrays(arrays, key=lambda x: x[0])) == [
        (0, 3), (1, 2), (1, 4), (3, 4), (4, 10), (5, 6)
    ]
    assert list(merge_sorted_arrays(arrays, key=lambda x: x[1])) == [
        (1, 2), (0, 3), (3, 4), (1, 4), (5, 6), (4, 10)
    ]