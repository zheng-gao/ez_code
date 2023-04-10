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
