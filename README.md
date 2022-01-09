# Package Installation
pip3 install eztree

# Package Releases
https://pypi.org/project/eztree/#history

# Examples

## Binary Tree Printer

```
from eztree.utils.printer import BinaryTreePrinter

class Node:
    def __init__(self, v=None, l=None, r=None):
        self.v = v
        self.l = l
        self.r = r

root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
printer.print(root)

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
```

## Random Binary Tree

```
from eztree.trees.random_binary_tree import RandomBinaryTree
tree = RandomBinaryTree(size=10, lower_bound=-5, upper_bound=10)
tree.print()

           ┌────────────(3)────────────┐           
    ┌────(-4)─────┐                   (5)─────┐    
 ┌─(8)         ┌─(6)                      ┌──(9)─┐ 
(6)          (-2)                        (2)    (2)

tree.make_tree()
tree.print()

        ┌────────────(6)────────────┐        
 ┌─────(7)─────┐             ┌─────(6)─────┐ 
(9)         ┌─(1)──┐        (9)        ┌──(3)
           (1)    (5)                (10)    
```

## Algorithm
### Traversals
```
from eztree.trees.binary_tree import BinaryTree
root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
tree.print()

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
     
print(f" Pre-Order: {tree.traversal('pre-order')}")
print(f"  In-Order: {tree.traversal('in-order')}")
print(f"Post-Order: {tree.traversal('post-order')}")

 Pre-Order: [0, 1, 3, 7, 4, 2, 5, 8, 9, 6]
  In-Order: [1, 3, 7, 4, 0, 2, 5, 8, 9, 6]
Post-Order: [1, 3, 7, 4, 2, 5, 8, 9, 6, 0]

```
### Lowest Common Ancestor
```
from eztree.trees.binary_tree import BinaryTree
root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
tree.print()

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         

n6, n7, n8 = root.r.r, root.l.l.r, root.r.l.l
tree.node_data(tree.lowest_common_ancestor([n6, n8]))
2
tree.node_data(tree.lowest_common_ancestor([n6, n7, n8]))
0
```
### Subtree Stats
```
from eztree.trees.binary_tree import BinaryTree
root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
tree.print()

            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    

print(f"Subtree Sum Min: {tree.subtree('sum-min')}")
print(f"Subtree Sum Max: {tree.subtree('sum-max')}")
print(f"Subtree Avg Min: {tree.subtree('avg-min')}")
print(f"Subtree Avg Max: {tree.subtree('avg-max')}")

Subtree Sum Min: -6
Subtree Sum Max: 19
Subtree Avg Min: -3.0
Subtree Avg Max: 10.0

```
### Max Path Sum
```
from eztree.trees.binary_tree import BinaryTree
root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
tree.print()

            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    

tree.max_path_sum()
19
```
### Depth & Balance
```
from eztree.trees.binary_tree import BinaryTree
root = Node(0, Node(0, Node(0), Node(0, r=Node(0))), Node(0, Node(0), Node(0, r=Node(0, l=Node(0)))))
tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
tree.print()

             ┌──────────────────────(0)──────────────────────┐                   
 ┌──────────(0)──────────┐                       ┌──────────(0)──────────┐       
(0)                     (0)────┐                (0)                     (0)────┐ 
                              (0)                                           ┌─(0)
                                                                           (0)   

tree.depth()
5
tree.is_balanced()
False

root = Node(0, Node(0, Node(0, l=Node(0)), Node(0, r=Node(0))), Node(0, Node(0), Node(0, l=Node(0))))
tree.root = root
tree.print()

          ┌──────────(0)──────────┐       
    ┌────(0)────┐           ┌────(0)────┐ 
 ┌─(0)         (0)─┐       (0)       ┌─(0)
(0)               (0)               (0)   

tree.depth()
4
tree.is_balanced()
True
```