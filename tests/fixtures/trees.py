from ezcode.trees.binary_tree import BinaryTree

class Node:
    def __init__(self, v=None, l=None, r=None):
        self.v = v
        self.l = l
        self.r = r

"""
Simple Tree:
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""
s_root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
s_tree = BinaryTree(root=s_root, data_name="v", left_name="l", right_name="r")

"""
Complex Tree:
            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    
"""
c_root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
c_tree = BinaryTree(root=c_root, data_name="v", left_name="l", right_name="r")
