from ezcode.tree.segment_tree import SegmentTree


def test_segment_tree():
    st = SegmentTree(merge=(lambda x,y:x+y))
    st.build_tree([2, 1, 5, 3, 4])
    assert st.query(1, 3) == 9
    st.update(index=2, data=7)
    assert st.query(1, 3) == 11