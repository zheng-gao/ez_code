from ezcode.Dynamic.SparseTable import SparseTable


def test_sparse_table():
    inf = float("inf")
    st = SparseTable(merge=max, data_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert st.range_query(6, 9) == 9
    assert st.range_query(2, 6) == 6
    assert st.range_query(2, 8) == 8
    assert st.dp_table == [
        [0,    1,    3,    7],
        [1,    2,    4,    8],
        [2,    3,    5,    9],
        [3,    4,    6,    8],
        [4,    5,    7,    7],
        [5,    6,    8,    8],
        [6,    7,    9, -inf],
        [7,    8,    8, -inf],
        [8,    9, -inf, -inf],
        [9, -inf, -inf, -inf],
    ]
    st.update(4, 7)
    assert st.dp_table == [
        [0,    1,    3,    7],
        [1,    2,    7,    8],
        [2,    3,    7,    9],
        [3,    7,    7,    8],
        [7,    7,    7,    7],
        [5,    6,    8,    8],
        [6,    7,    9, -inf],
        [7,    8,    8, -inf],
        [8,    9, -inf, -inf],
        [9, -inf, -inf, -inf],
    ]
    st.update(6, 10)
    assert st.dp_table == [
        [ 0,    1,    3,   10],
        [ 1,    2,    7,   10],
        [ 2,    3,    7,   10],
        [ 3,    7,   10,   10],
        [ 7,    7,   10,   10],
        [ 5,   10,   10,   10],
        [10,   10,   10, -inf],
        [ 7,    8,    8, -inf],
        [ 8,    9, -inf, -inf],
        [ 9, -inf, -inf, -inf],
    ]
    assert st.range_query(0, 5) == 7
    assert st.range_query(2, 5) == 7
    assert st.range_query(3, 8) == 10
    assert st.range_query(0, 8) == 10
    assert st.range_query(5, 9) == 10
    st = SparseTable(merge=min)
    st.build_table(data_list=[3, 2, 4, 5, 6, 8, 1, 9, 7, 0])
    assert st.range_query(0, 3) == 2
    assert st.range_query(2, 8) == 1
    assert st.range_query(3, 7) == 1
    assert st.range_query(4, 7) == 1
    assert st.range_query(7, 9) == 0
    assert st.range_query(7, 8) == 7
    assert st.range_query(0, 9) == 0
    assert st.range_query(2, 4) == 4
    assert st.dp_table == [
        [3,   2,   2,   1],
        [2,   2,   2,   1],
        [4,   4,   4,   0],
        [5,   5,   1,   1],
        [6,   6,   1,   1],
        [8,   1,   1,   1],
        [1,   1,   0, inf],
        [9,   7,   7, inf],
        [7,   0, inf, inf],
        [0, inf, inf, inf]
    ]
    st.update(1, 1)
    assert st.dp_table == [
        [3,   1,   1,   1],
        [1,   1,   1,   1],
        [4,   4,   4,   0],
        [5,   5,   1,   1],
        [6,   6,   1,   1],
        [8,   1,   1,   1],
        [1,   1,   0, inf],
        [9,   7,   7, inf],
        [7,   0, inf, inf],
        [0, inf, inf, inf]
    ]
    assert st.range_query(0, 3) == 1
    assert st.range_query(1, 5) == 1
    st.update(6, 10)
    assert st.dp_table == [
        [ 3,   1,   1,   1],
        [ 1,   1,   1,   1],
        [ 4,   4,   4,   0],
        [ 5,   5,   5,   5],
        [ 6,   6,   6,   6],
        [ 8,   8,   7,   7],
        [10,   9,   0, inf],
        [ 9,   7,   7, inf],
        [ 7,   0, inf, inf],
        [ 0, inf, inf, inf]
    ]
    assert st.range_query(2, 8) == 4
    assert st.range_query(5, 7) == 8
    assert st.range_query(4, 9) == 0




