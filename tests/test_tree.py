from fixture.tree import printer, s_root, s_tree, c_tree, s_tree_string, c_tree_string
from fixture.tree import trie, trie_string, suffix_trie, suffix_trie_string
from fixture.utils import check_list_copy


def test_printer():
    assert s_tree_string == printer.to_string(s_tree.root)
    assert c_tree_string == printer.to_string(c_tree.root)


def test_traversals():
    assert [0, 1, 3, 7, 4, 2, 5, 8, 9, 6] == s_tree.traversal('pre-order')
    assert [1, 3, 7, 4, 0, 2, 5, 8, 9, 6] == s_tree.traversal('in-order')
    assert [1, 3, 7, 4, 2, 5, 8, 9, 6, 0] == s_tree.traversal('post-order')


def test_lowest_common_ancestor():
    s6, s7, s8 = s_root.right.right, s_root.left.left.right, s_root.right.left.left
    assert 2 == s_tree.node_data(s_tree.lowest_common_ancestor([s6, s8]))
    assert 0 == s_tree.node_data(s_tree.lowest_common_ancestor([s6, s7, s8]))


def test_subtree_stats():
    assert c_tree.subtree('sum-min') == -6
    assert c_tree.subtree('sum-max') == 19
    assert c_tree.subtree('avg-min') == -3
    assert c_tree.subtree('avg-max') == 10


def test_depth():
    assert s_tree.depth() == 4
    assert c_tree.depth() == 4


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
    assert check_list_copy(trie.prefix_wildcard(list("co")), [list("cod"), list("code"), list("coke"), list("coffee")])


def test_suffix_trie():
    assert str(suffix_trie) == suffix_trie_string

