from ezcode.tree.binary_tree import BinaryTree
from ezcode.tree.printer import BinaryTreePrinter


class Node:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"


s_root = Node(0, Node(1, Node(3, right=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
s_tree = BinaryTree(root=s_root, data_name="value", left_name="left", right_name="right")
s_tree_string = """
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""[1:]

c_root = Node(-2, Node(8, Node(-4, left=Node(-2)), Node(3, left=Node(-1))), Node(-3, left=Node(2, Node(10), Node(7))))
c_tree = BinaryTree(root=c_root, data_name="value", left_name="left", right_name="right")
c_tree_string = """
            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    
"""[1:]


def test_printer():
    printer = BinaryTreePrinter(data_name="value", left_name="left", right_name="right")
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


def test_remove_bst_node():
    bst_root = Node(1, Node(0), Node(6, Node(5, Node(3, Node(2), Node(4))), Node(7, right=Node(9, Node(8), Node(10)))))
    bst = BinaryTree(root=bst_root, data_name="value", left_name="left", right_name="right")
    printer = BinaryTreePrinter(data_name="value", left_name="left", right_name="right")
    assert printer.to_string(bst.root) == """
 ┌──────────────────────────(1)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                ┌──(3)─┐                                  ┌──(9)─┐ 
                               (2)    (4)                                (8)   (10)
"""[1:]
    bst.remove_bst_node(1)
    assert printer.to_string(bst.root) == """
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                   (3)─┐                                  ┌──(9)─┐ 
                                      (4)                                (8)   (10)
"""[1:]
    bst.remove_bst_node(5)
    assert printer.to_string(bst.root) == """
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                          (3)─────┐                   (7)─────┐    
                                                 (4)                      ┌──(9)─┐ 
                                                                         (8)   (10)
"""[1:]
    bst.remove_bst_node(6)
    assert printer.to_string(bst.root) == """
 ┌────────────(2)────────────┐           
(0)                   ┌─────(7)─────┐    
                     (3)─┐      ┌──(9)─┐ 
                        (4)    (8)   (10)
"""[1:]
    bst.remove_bst_node(10)
    assert printer.to_string(bst.root) == """
 ┌──────────(2)──────────┐       
(0)                ┌────(7)────┐ 
                  (3)─┐     ┌─(9)
                     (4)   (8)   
"""[1:]
    bst.remove_bst_node(2)
    assert printer.to_string(bst.root) == """
 ┌──────────(3)──────────┐       
(0)                ┌────(7)────┐ 
                  (4)       ┌─(9)
                           (8)   
"""[1:]
    bst.remove_bst_node(3)
    assert printer.to_string(bst.root) == """
 ┌──────────(4)──────────┐       
(0)                     (7)────┐ 
                            ┌─(9)
                           (8)   
"""[1:]
    bst.remove_bst_node(0)
    assert printer.to_string(bst.root) == """
(4)──────────┐       
            (7)────┐ 
                ┌─(9)
               (8)   
"""[1:]
    bst.remove_bst_node(4)
    assert printer.to_string(bst.root) == """
(7)────┐ 
    ┌─(9)
   (8)   
"""[1:]
    bst.remove_bst_node(9)
    assert printer.to_string(bst.root) == """
(7)─┐ 
   (8)
"""[1:]
    bst.remove_bst_node(7)
    assert printer.to_string(bst.root) == """
(8)
"""[1:]
    bst.remove_bst_node(8)
    assert printer.to_string(bst.root) == """
None
"""[1:]


def test_remove_bst_nodes():
    bst_root = Node(5, Node(3, Node(1, Node(0), Node(2)), Node(4)), Node(8, Node(6, right=Node(7)), Node(9, right=Node(10))))
    bst = BinaryTree(root=bst_root, data_name="value", left_name="left", right_name="right")
    printer = BinaryTreePrinter(data_name="value", left_name="left", right_name="right")
    assert printer.to_string(bst.root) == """
           ┌────────────(5)────────────┐           
    ┌─────(3)─────┐             ┌─────(8)─────┐    
 ┌─(1)──┐        (4)           (6)─┐         (9)─┐ 
(0)    (2)                        (7)          (10)
"""[1:]
    bst.remove_bst_nodes(1, 4)
    assert printer.to_string(bst.root) == """
 ┌────────────(5)────────────┐           
(0)                   ┌─────(8)─────┐    
                     (6)─┐         (9)─┐ 
                        (7)          (10)
"""[1:]
    bst.remove_bst_nodes(7, 9)
    assert printer.to_string(bst.root) == """
 ┌─────(5)─────┐ 
(0)        ┌─(10)
          (6)    
"""[1:]
    bst.remove_bst_nodes(3, 8)
    assert printer.to_string(bst.root) == """
 ┌(10)
(0)   
"""[1:]
    bst.remove_bst_nodes(5, 20)
    assert printer.to_string(bst.root) == """
(0)
"""[1:]
    bst.remove_bst_nodes(-1, 1)
    assert printer.to_string(bst.root) == """
None
"""[1:]
    bst_root = Node(5, Node(3, Node(1, Node(0), Node(2)), Node(4)), Node(8, Node(6, right=Node(7)), Node(9, right=Node(10))))
    bst = BinaryTree(root=bst_root, data_name="value", left_name="left", right_name="right")
    bst.remove_bst_nodes(4, 7)
    assert printer.to_string(bst.root) == """
           ┌────────────(8)────────────┐        
    ┌─────(3)                         (9)─────┐ 
 ┌─(1)──┐                                   (10)
(0)    (2)                                      
"""[1:]
    bst.remove_bst_nodes(2, 5)
    assert printer.to_string(bst.root) == """
    ┌─────(8)─────┐    
 ┌─(1)           (9)─┐ 
(0)                (10)
"""[1:]
    bst.remove_bst_nodes(3, 15)
    assert printer.to_string(bst.root) == """
 ┌─(1)
(0)   
"""[1:]
    bst.remove_bst_nodes(0, 3)
    assert printer.to_string(bst.root) == """
None
"""[1:]
