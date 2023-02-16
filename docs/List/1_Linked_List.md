# Linked List
## Overview

The class [LinkedList](../../src/ezcode/List/LinkedList.py#L10) is inherited from [collection.abc.MutableSequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence)

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








