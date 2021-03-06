from ezcode.tree.forest import DisjointSets
from ezcode.tree.binary_tree import SegmentTree
from fixture.tree import printer, s_root, s_tree, c_tree, s_tree_string, c_tree_string
from fixture.tree import trie, trie_string, suffix_trie, suffix_trie_string
from fixture.utils import equal_list


def test_printer():
    assert s_tree_string == printer.to_string(s_tree.root)
    assert c_tree_string == printer.to_string(c_tree.root)


def test_traversals():
    assert [0, 1, 3, 7, 4, 2, 5, 8, 9, 6] == s_tree.traversal("pre-order")
    assert [1, 3, 7, 4, 0, 2, 5, 8, 9, 6] == s_tree.traversal("in-order")
    assert [1, 3, 7, 4, 2, 5, 8, 9, 6, 0] == s_tree.traversal("post-order")
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == s_tree.traversal("level-order")
    level_order_left_most_nodes = list()
    s_tree.algorithm.level_order(s_tree.root, level_order_left_most_nodes, left_most_nodes=True)
    assert [0, 1, 3, 7] == level_order_left_most_nodes

def test_lowest_common_ancestor():
    s6, s7, s8 = s_root.right.right, s_root.left.left.right, s_root.right.left.left
    assert 2 == s_tree.get_data(s_tree.lowest_common_ancestor([s6, s8]))
    assert 0 == s_tree.get_data(s_tree.lowest_common_ancestor([s6, s7, s8]))


def test_subtree_stats():
    assert c_tree.subtree('sum-min') == -6
    assert c_tree.subtree('sum-max') == 19
    assert c_tree.subtree('avg-min') == -3
    assert c_tree.subtree('avg-max') == 10


def test_depth():
    assert s_tree.depth() == 4
    assert s_tree.algorithm.level_order(s_tree.root) == 4
    assert c_tree.depth() == 4
    assert c_tree.algorithm.level_order(c_tree.root) == 4


def test_is_balanced():
    assert s_tree.is_balanced() is True
    assert c_tree.is_balanced() is False


def test_max_path_sum():
    assert s_tree.max_path_sum() == 27
    assert c_tree.max_path_sum() == 19


def test_is_copied():
    assert s_tree.is_copied(s_tree)
    assert c_tree.is_copied(c_tree)


def test_copy():
    assert s_tree.is_copied(s_tree.copy())
    assert c_tree.is_copied(c_tree.copy())


def test_serialization():
    assert s_tree.serialize() == "0,1,2,3,4,5,6,None,7,None,None,8,9,None,None,None,None,None,None,None,None"
    assert c_tree.serialize() == "-2,8,-3,-4,3,2,None,-2,None,-1,None,10,7,None,None,None,None,None,None,None,None"


def test_deserialization():
    assert s_tree.is_copied(s_tree.deserialize(formatter=int, string=s_tree.serialize()))
    assert c_tree.is_copied(c_tree.deserialize(formatter=int, string=c_tree.serialize()))


def test_trie():
    assert str(trie) == trie_string
    assert trie.size() == 4
    assert trie.longest_common_prefix() == list("co")
    assert trie.contains("cof")
    assert not trie.contains("cofe")
    assert trie.contains("coffee", strict=True)
    assert not trie.contains("cof", strict=True)
    assert equal_list(trie.prefix_wildcard(list("co")), [list("cod"), list("code"), list("coke"), list("coffee")])


def test_suffix_trie():
    assert str(suffix_trie) == suffix_trie_string


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


def test_segment_tree():
    st = SegmentTree(merge=(lambda x,y:x+y))
    st.build_tree([2, 1, 5, 3, 4])
    assert st.query(1, 3) == 9
    st.update(index=2, data=7)
    assert st.query(1, 3) == 11

