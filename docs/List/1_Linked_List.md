# Linked List
## Overview

The class [LinkedList](../../src/ezcode/List/LinkedList.py#L10) is inherited from collection.abc.MutableSequence
class LinkedList(MutableSequence):
    def __init__(self,
        init_data: Iterable = None,
        head=None,
        head_copy=None,
        data_name: str = DATA_NAME,
        next_name: str = NEXT_NAME
    )
    def _size(self)  # recalculate the size: Time: O(N)
    def new_node(self, data=None, next_node=None)
    def node_to_string(self, node) -> str
    def get_data(self, node)
    def set_data(self, node, data)
    def get_next(self, node, steps: int = 1)
    def has_next(self, node, steps: int = 1) -> bool
    def set_next(self, node, next_node=None)
    def __iter__(self)
    def __reversed__(self)
    def __contains__(self, data)
    def __len__(self) -> int:
    def __getitem__(self, index: int)
    def __setitem__(self, index: int, data)
    def __delitem__(self, index: int)
    def __add__(self, other: Iterable)
    def __iadd__(self, other: Iterable)
    def __radd__(self, other: Iterable)
    def __str__(self) -> str
    def print(self,
    	reverse: bool = False,
    	include_end: bool = True,
    	mark_head: bool = True,
        forward_link: str = FORWARD_LINK,
        backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    )
    def to_string(self,
        reverse: bool = False,
        include_end: bool = True,
        mark_head: bool = True,
        forward_link: str = FORWARD_LINK,
        backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    )
    def regularize_index(self, index: int, auto_fit: bool = False)
    def get_node(self, index: int)
    def clear(self)
    def count(self, data)
    def copy(self) -> LinkedList
    def copy_from_node(self, node)
    def copy_from(self, other)
    def extend(self, other: Iterable)
    def append(self, data)
    def append_node(self, node)
    def insert(self, index: int, data)
    def remove_all(self, data)  # data can be a container or value
    def reverse(self)
    def pop(self)
    def equal(self, other) -> bool
    def has_cycle(self, node) -> bool
    def get_cycle_entrance(self, node)
    def swap_pairs_of_nodes(self)
---
## Examples
### Initialize List via Custom Data Structure
```python
>>> from ezcode import LinkedList
>>> class Node:
...     def __init__(self, v=None, n=None):
...         self.v = v
...         self.n = n
... 
>>> l = LinkedList(head=Node(0, Node(1, Node(2, Node(3)))), data_name="v", next_name="n")
>>> print(l)
None <─ 3 <─ 2 <─ 1 <─ 0 (H)
```
### Initialize List via Iterables
```python
>>> from ezcode import LinkedList
>>> LinkedList([0, 1, 2, 3]).print()
None <─ 0 <─ 1 <─ 2 <─ 3 (H)
```
### Iterator
```python
>>> from ezcode import LinkedList
>>> l = LinkedList([0, 1, 2, 3])
>>> list(iter(l))
[0, 1, 2, 3]
>>> list(reversed(l))
[3, 2, 1, 0]
```
### Get, Set & Delete
```python
>>> from ezcode import LinkedList
>>> l = LinkedList([0, 1, 2, 3])
>>> print(l[2])
2
>>> l[1] = -1
>>> l.print()
None <─ 0 <─ -1 <─ 2 <─ 3 (H)
>>> del l[-1]
>>> l.print()
None <─ 0 <─ -1 <─ 2 (H)
```
### Append & Pop
```python
>>> from ezcode import LinkedList
>>> l = LinkedList()
>>> for i in range(4):
...     l.append(i)
... 
>>> l.print()
None <─ 0 <─ 1 <─ 2 <─ 3 (H)
>>> while len(l) > 0:
...     print(l.pop(), end=" ")
... 
3 2 1 0
```








