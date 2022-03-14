# Binary Tree

## Binary Tree Printer

```python
>>> class Node:
...     def __init__(self, v=None, l=None, r=None):
...         self.v = v
...         self.l = l
...         self.r = r
... 
>>> from ezcode.tree.printer import BinaryTreePrinter
>>> root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
>>> printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
>>> printer.print(root)

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
```

## Random Binary Tree

```python
>>> from ezcode.tree.binary_tree import RandomBinaryTree
>>> tree = RandomBinaryTree(size=10, lower_bound=-5, upper_bound=10)
>>> tree.print()

           ┌────────────(3)────────────┐           
    ┌────(-4)─────┐                   (5)─────┐    
 ┌─(8)         ┌─(6)                      ┌──(9)─┐ 
(6)          (-2)                        (2)    (2)

>>> tree.make_tree()
>>> tree.print()

        ┌────────────(6)────────────┐        
 ┌─────(7)─────┐             ┌─────(6)─────┐ 
(9)         ┌─(1)──┐        (9)        ┌──(3)
           (1)    (5)                (10)    
```

## Algorithm

### Traversals

```python
>>> from ezcode.tree.binary_tree import BinaryTree
>>> root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
     
>>> print(f"  Pre-Order: {tree.traversal('pre-order')}")
>>> print(f"   In-Order: {tree.traversal('in-order')}")
>>> print(f" Post-Order: {tree.traversal('post-order')}")
>>> print(f"Level-Order: {tree.traversal('level-order')}")

  Pre-Order: [0, 1, 3, 7, 4, 2, 5, 8, 9, 6]
   In-Order: [1, 3, 7, 4, 0, 2, 5, 8, 9, 6]
 Post-Order: [1, 3, 7, 4, 2, 5, 8, 9, 6, 0]
Level-Order: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Lowest Common Ancestor

```python
>>> from ezcode.tree.binary_tree import BinaryTree
>>> root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         

>>> n6, n7, n8 = root.r.r, root.l.l.r, root.r.l.l
>>> tree.node_data(tree.lowest_common_ancestor([n6, n8]))
2
>>> tree.node_data(tree.lowest_common_ancestor([n6, n7, n8]))
0
```

### Subtree Stats

```python
>>> from ezcode.tree.binary_tree import BinaryTree
>>> root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    

>>> print(f"Subtree Sum Min: {tree.subtree('sum-min')}")
>>> print(f"Subtree Sum Max: {tree.subtree('sum-max')}")
>>> print(f"Subtree Avg Min: {tree.subtree('avg-min')}")
>>> print(f"Subtree Avg Max: {tree.subtree('avg-max')}")

Subtree Sum Min: -6
Subtree Sum Max: 19
Subtree Avg Min: -3.0
Subtree Avg Max: 10.0

```

### Max Path Sum

```python
>>> from ezcode.tree.binary_tree import BinaryTree
>>> root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    

>>> tree.max_path_sum()
19
```

### Depth & Balance

```python
>>> from ezcode.tree.binary_tree import BinaryTree
>>> root = Node(0, Node(0, Node(0), Node(0, r=Node(0))), Node(0, Node(0), Node(0, r=Node(0, l=Node(0)))))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

             ┌──────────────────────(0)──────────────────────┐                   
 ┌──────────(0)──────────┐                       ┌──────────(0)──────────┐       
(0)                     (0)────┐                (0)                     (0)────┐ 
                              (0)                                           ┌─(0)
                                                                           (0)   

>>> [tree.depth(), tree.is_balanced()]
[5, False]

>>> root = Node(0, Node(0, Node(0, l=Node(0)), Node(0, r=Node(0))), Node(0, Node(0), Node(0, l=Node(0))))
>>> tree.root = root
>>> tree.print()

          ┌──────────(0)──────────┐       
    ┌────(0)────┐           ┌────(0)────┐ 
 ┌─(0)         (0)─┐       (0)       ┌─(0)
(0)               (0)               (0)   

>>> [tree.depth(), tree.is_balanced()]
[4, True]
```

### Serialization & Deserialization

```python
>>> from ezcode.tree.printer import BinaryTreePrinter
>>> from ezcode.tree.binary_tree import BinaryTree
>>> printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
>>> root = Node(1, Node(2), Node(3, Node(4), Node(5)))
>>> tree = BinaryTree(root, data_name="v", left_name="l", right_name="r")
>>> tree.print()

 ┌────(1)────┐    
(2)       ┌─(3)─┐ 
         (4)   (5)

>>> serialized = tree.serialize(delimiter=",")
>>> print(serialized)

1,2,3,None,None,4,5,None,None,None,None

>>> printer.print(tree.deserialize(formatter=int, string=serialized, delimiter=","))

 ┌────(1)────┐    
(2)       ┌─(3)─┐ 
         (4)   (5)
```

# Trie
```python
>>> from ezcode.tree.trie import Trie
>>> trie = Trie()
>>> for word in ["today", "tomorrow", "tonight", "tobaco", "tod", "tony"]:
...     trie.add(list(word))
... 
>>> trie.size()
6
>>> trie.print()
^:6 -> t:6 -> o:6 -> d:2:$ -> a:1 -> y:1:$
^:6 -> t:6 -> o:6 -> m:1 -> o:1 -> r:1 -> r:1 -> o:1 -> w:1:$
^:6 -> t:6 -> o:6 -> n:2 -> i:1 -> g:1 -> h:1 -> t:1:$
^:6 -> t:6 -> o:6 -> n:2 -> y:1:$
^:6 -> t:6 -> o:6 -> b:1 -> a:1 -> c:1 -> o:1:$
>>> trie.contains(list("toni"))
True
>>> trie.contains(list("tonx"))
False
>>> trie.contains(list("toni"), strict=True)
False
>>> trie.contains(list("tod"), strict=True)
True
>>> "".join(trie.longest_common_prefix())
'to'
>>> for word in trie.prefix_wildcard(list("ton")):
...     print("".join(word))
... 
tonight
tony
```
# Suffix Trie
```python
>>> from ezcode.tree.trie import SuffixTrie
>>> suffix_trie = SuffixTrie("abcab")
>>> suffix_trie.print()
^:5 -> a:2 -> b:2:$ -> c:1 -> a:1 -> b:1:$
^:5 -> b:2:$ -> c:1 -> a:1 -> b:1:$
^:5 -> c:1 -> a:1 -> b:1:$
```