from ezcode.Container.Tree.BinaryTree import BinaryTree, BinaryTreePrinter, BinaryTreeIterator


class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


s_root = Node(0, Node(1, Node(3, right=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
s_tree = BinaryTree(root_copy=s_root, data_name="value", left_name="left", right_name="right")

c_root = Node(-2, Node(8, Node(-4, left=Node(-2)), Node(3, left=Node(-1))), Node(-3, left=Node(2, Node(10), Node(7))))
c_tree = BinaryTree(root_copy=c_root, data_name="value", left_name="left", right_name="right")


def test_binary_tree_printer():
    printer = BinaryTreePrinter(data_name="value", left_name="left", right_name="right")
    assert printer.to_string(s_tree.root) == """
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""[1:]
    assert printer.to_string(c_tree.root) == """
            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    
"""[1:]


def test_binary_tree_traversals():
    assert [0, 1, 3, 7, 4, 2, 5, 8, 9, 6] == s_tree.traversal("pre-order")
    assert [3, 7, 1, 4, 0, 8, 5, 9, 2, 6] == s_tree.traversal("in-order")
    assert [7, 3, 4, 1, 8, 9, 5, 6, 2, 0] == s_tree.traversal("post-order")
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == s_tree.traversal("level-order")
    level_order_left_most_nodes = list()
    s_tree.algorithm.level_order(s_tree.root, level_order_left_most_nodes, left_most_nodes=True)
    assert [0, 1, 3, 7] == level_order_left_most_nodes


def test_binary_tree_iterator():
    assert [0, 1, 3, 7, 4, 2, 5, 8, 9, 6] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.PRE_ORDER, is_left_first=True, data_name="value"))
    assert [0, 2, 6, 5, 9, 8, 1, 4, 3, 7] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.PRE_ORDER, is_left_first=False, data_name="value"))
    assert [3, 7, 1, 4, 0, 8, 5, 9, 2, 6] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.IN_ORDER, is_left_first=True, data_name="value"))
    assert [6, 2, 9, 5, 8, 0, 4, 1, 7, 3] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.IN_ORDER, is_left_first=False, data_name="value"))
    assert [7, 3, 4, 1, 8, 9, 5, 6, 2, 0] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.POST_ORDER, is_left_first=True, data_name="value"))
    assert [6, 9, 8, 5, 2, 4, 7, 3, 1, 0] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.POST_ORDER, is_left_first=False, data_name="value"))
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.BFS, is_left_first=True, data_name="value"))
    assert [0, 2, 1, 6, 5, 4, 3, 9, 8, 7] == list(BinaryTreeIterator(
        s_tree.root, mode=BinaryTreeIterator.Mode.BFS, is_left_first=False, data_name="value"))


def test_binary_tree_size():
    assert len(s_tree) == 10
    assert len(c_tree) == 10
    assert len(BinaryTree()) == 0
    assert len(BinaryTree(root_copy=s_tree.root, data_name="value", left_name="left", right_name="right")) == 10
    assert len(BinaryTree([1, 2, 3], root_copy=s_tree.root, data_name="value", left_name="left", right_name="right")) == 13


def test_binary_tree_contains():
    for i in range(10):
        assert i in s_tree
    for i in [-1, 10]:
        assert i not in s_tree
    for i in [-1, -2, -3, -4, 2, 3, 7, 8, 10]:
        assert i in c_tree
    assert 0 not in c_tree


def test_binary_tree_depth():
    assert s_tree.get_depth(s_tree.root) == 1
    assert s_tree.get_depth(s_tree.root.right) == 2
    assert s_tree.get_depth(s_tree.root.left.right) == 3
    assert s_tree.get_depth(s_tree.root.left.left.right) == 4
    assert s_tree.get_depth(s_tree.root.left.left.right.left) == 0
    assert s_tree.get_depth(None) == 0
    assert s_tree.get_depth(Node(0)) == 0
    assert BinaryTree().get_depth(None) == 0


def test_binary_tree_lowest_common_ancestor():
    s6 = s_tree.root.right.right
    s7 = s_tree.root.left.left.right
    s8 = s_tree.root.right.left.left
    """
           ┌──────────(0)──────────┐       
     ┌────(1)────┐           ┌────(2)────┐ 
    (3)─┐       (4)       ┌─(5)─┐       (6)
       (7)               (8)   (9)         
    """
    assert s_tree.root.right == s_tree.lowest_common_ancestor([s6, s8])
    assert s_tree.root == s_tree.lowest_common_ancestor([s6, s7, s8])


def test_binary_tree_subtree_stats():
    assert c_tree.subtree('sum-min') == -6
    assert c_tree.subtree('sum-max') == 19
    assert c_tree.subtree('avg-min') == -3
    assert c_tree.subtree('avg-max') == 10


def test_binary_tree_height():
    assert s_tree.height() == 4
    assert s_tree.algorithm.level_order(s_tree.root) == 4
    assert c_tree.height() == 4
    assert c_tree.algorithm.level_order(c_tree.root) == 4


def test_binary_tree_is_balanced():
    assert s_tree.is_balanced() is True
    assert c_tree.is_balanced() is False


def test_binary_tree_max_path_sum():
    assert s_tree.max_path_sum() == 27
    assert c_tree.max_path_sum() == 19


def test_binary_tree_is_copied():
    assert s_tree == s_tree
    assert c_tree == c_tree


def test_binary_tree_copy():
    assert s_tree == s_tree.copy()
    assert c_tree == c_tree.copy()


def test_binary_tree_serialization():
    assert s_tree.serialize() == "0,1,2,3,4,5,6,None,7,None,None,8,9,None,None,None,None,None,None,None,None"
    assert c_tree.serialize() == "-2,8,-3,-4,3,2,None,-2,None,-1,None,10,7,None,None,None,None,None,None,None,None"


def test_binary_tree_deserialization():
    assert s_tree == s_tree.deserialize(formatter=int, string=s_tree.serialize())
    assert c_tree == c_tree.deserialize(formatter=int, string=c_tree.serialize())


