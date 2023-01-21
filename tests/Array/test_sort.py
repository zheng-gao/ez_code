from ezcode.Array.Sort import quick_sort


def test_quick_sort():
    data_1 = [7, 2, 4, 6, 5, 4, 1, 3, 8, 0, 6, 9, 4]
    data_2 = data_1.copy()
    quick_sort(data_1, reverse=False)
    quick_sort(data_2, reverse=True)
    assert data_1 == [0, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 9]
    assert data_2 == [9, 8, 7, 6, 6, 5, 4, 4, 4, 3, 2, 1, 0]

