from ezcode.Tree.SegmentTree import SegmentTree


def test_segment_tree():
    st = SegmentTree([2, 1, 5, 3, 4], merge=lambda x, y: x + y)
    assert st.query(1, 3) == 9
    st.update(index=2, data=7)
    assert st.query(1, 3) == 11