import pytest

from fixtures.trees import s_root, s_tree, c_tree

"""
Simple Tree:
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""

def test_traversals():
    assert [0, 1, 3, 7, 4, 2, 5, 8, 9, 6] == s_tree.traversal('pre-order')
    assert [1, 3, 7, 4, 0, 2, 5, 8, 9, 6] == s_tree.traversal('in-order')
    assert [1, 3, 7, 4, 2, 5, 8, 9, 6, 0] == s_tree.traversal('post-order')


def test_lowest_common_ancestor():
    s6, s7, s8 = s_root.r.r, s_root.l.l.r, s_root.r.l.l
    assert 2 == s_tree.node_data(s_tree.lowest_common_ancestor([s6, s8]))
    assert 0 == s_tree.node_data(s_tree.lowest_common_ancestor([s6, s7, s8]))

"""
Complex Tree:
            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    
"""

def test_subtree_stats():
    assert c_tree.subtree('sum-min') == -6
    assert c_tree.subtree('sum-max') == 19
    assert c_tree.subtree('avg-min') == -3
    assert c_tree.subtree('avg-max') == 10


def test_find_depth():
    assert s_tree.depth() == 4
    assert c_tree.depth() == 4


def test_is_balanced():
    assert s_tree.is_balanced() == True
    assert c_tree.is_balanced() == False

def test_max_path_sum():
    assert s_tree.max_path_sum() == 27
    assert c_tree.max_path_sum() == 19
