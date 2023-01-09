# Binary Tree

## Binary Tree Printer

```python
>>> class Node:
...     def __init__(self, v=None, l=None, r=None):
...         self.v = v
...         self.l = l
...         self.r = r
... 
>>> from ezcode.tree.BinaryTree import BinaryTreePrinter
>>> root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
>>> printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
>>> printer.print(root)

       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
```


## Algorithm

### Traversals

```python
>>> from ezcode.tree.BinaryTree import BinaryTree
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





# Forest

## Disjoint Sets
```python
>>> from ezcode.tree.forest import DisjointSets
>>> ds = DisjointSets(set([0, 1, 2, 3, 4, 5, 6]))
>>> ds.get_max_set_size()
1
>>> len(ds)
7
>>> ds.union(3, 4)
True
>>> ds.union(1, 0)
True
>>> ds.union(4, 1)
True
>>> ds.get_max_set_size()
4
>>> ds.union(4, 0)
False
>>> ds.union(5, 2)
True
>>> len(ds)
3
>>> ds.is_joint(1, 4)
True
>>> ds.is_joint(1, 2)
False
>>> ds.get_set_size(2)
2
>>> ds.get_set_size(1)
4
>>> ds.union(2, 3)
True
>>> ds.get_max_set_size()
6
>>> len(ds)
2
>>> ds.is_joint(1, 2)
True
>>> ds.is_joint(1, 6)
False
>>> ds.get_set_size(2)
6
>>> ds.get_set_size(6)
1
```


## File System
```python
>>> from ezcode.tree.file_system import FileSystem
>>> fs = FileSystem()
>>> fs.mkdir("/var/tmp", True)
>>> fs.echo_to("/var/tmp/test.txt", "hello world")
>>> fs.cd("/var/tmp")
>>> fs.pwd()
/var/tmp
>>> fs.ls()
[f] test.txt
>>> fs.cat("test.txt")
hello world
>>> fs.cd("../..")
>>> fs.pwd()
/
>>> fs.mkdir("/home")
>>> for user in ["user_1", "user_2", "user_3"]:
...     fs.mkdir(f"/home/{user}")
...     fs.touch(f"/home/{user}/.profile")
...     fs.echo_to(f"/home/{user}/.profile", f"ID={user}")
...
>>> fs.ls("/")
[d] home
[d] var
>>> fs.cd("/home")
>>> fs.pwd()
/home
>>> fs.ls()
[d] user_1
[d] user_2
[d] user_3
>>> fs.cd("user_1")
>>> fs.echo_to("test.txt", "hello user_1")
>>> fs.pwd()
/home/user_1
>>> fs.ls()
[f] .profile
[f] test.txt
>>> fs.cat(".profile")
ID=user_1
>>> fs.cat("/home/user_3/.profile")
ID=user_3
>>> fs.ls("/home/user_3")
[f] .profile
>>> fs.rm("/home/user_3")
>>> fs.cd("..")
>>> fs.pwd()
/home
>>> fs.cat("user_1/test.txt")
hello user_1
>>> fs.ls()
[d] user_1
[d] user_2
>>> fs.cd("..")
>>> fs.pwd()
/
>>> fs.tree("home")
home
├── user_1
│   ├── .profile
│   └── test.txt
└── user_2
    └── .profile
>>> fs.tree()
/
├── home
│   ├── user_1
│   │   ├── .profile
│   │   └── test.txt
│   └── user_2
│       └── .profile
└── var
    └── tmp
        └── test.txt
>>> fs.tree("/", 2)
/
├── home
│   ├── user_1
│   └── user_2
└── var
    └── tmp
```
