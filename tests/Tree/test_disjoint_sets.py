from ezcode.Tree.disjoint_sets import DisjointSets


def test_disjoint_sets():
    ds = DisjointSets(set([0, 1, 2, 3, 4, 5, 6]))
    assert ds.get_max_set_size() == 1
    assert len(ds) == 7
    assert ds.union(3, 4)
    assert ds.union(1, 0)
    assert ds.union(4, 1)
    assert ds.get_max_set_size() == 4
    assert not ds.union(4, 0)
    assert ds.union(5, 2)
    assert len(ds) == 3
    assert ds.is_joint(1, 4)
    assert not ds.is_joint(1, 2)
    assert ds.get_set_size(2) == 2
    assert ds.get_set_size(1) == 4
    assert ds.union(2, 3)
    assert ds.get_max_set_size() == 6
    assert len(ds) == 2
    assert ds.is_joint(1, 2)
    assert not ds.is_joint(1, 6)
    assert ds.get_set_size(2) == 6
    assert ds.get_set_size(6) == 1
