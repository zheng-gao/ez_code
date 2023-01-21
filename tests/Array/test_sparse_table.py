from ezcode.Array.SparseTable import SparseTable


def test_sparse_table():
    st = SparseTable(merge=max, data_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert st.range_query(6, 9) == 9
    assert st.range_query(2, 6) == 6
    assert st.range_query(2, 8) == 8
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

