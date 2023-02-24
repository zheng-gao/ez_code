# Doubly Linked List
## Overview

[ezcode.List](../../src/ezcode/List/__init__.py).[DoublyLinkedList](../../src/ezcode/List/DoublyLinkedList.py#L10) inherits from [ezcode.List.TailedLinkedList](../../src/ezcode/List/TailedLinkedList.py#L9). It maintains both head and tail pointers and every node has 2 pointers to both of its successor and predecessor. Nodes can be appended or poped from both sides.

## Details
### Iterator
```python
>>> from ezcode import DoublyLinkedList
>>> l = DoublyLinkedList([0, 1, 2, 3])
>>> list(iter(l))
[0, 1, 2, 3]
>>> list(reversed(l))
[3, 2, 1, 0]
```
### Append, Append Left, Pop & Pop Left
```python
>>> from ezcode import DoublyLinkedList
>>> l = DoublyLinkedList()
>>> for i in range(3):
...     l.append(i)
... 
>>> for i in range(3, 6):
...     l.appendleft(i)
... 
>>> l.print()
None <─ (T) 5 <─> 4 <─> 3 <─> 0 <─> 1 <─> 2 (H) ─> None
>>> while len(l) > 3:
...     print(l.pop(), end=" ")
... 
2 1 0
>>> while len(l) > 0:
...     print(l.popleft(), end=" ")
... 
5 4 3
```
### Reverse & Copy
```python
>>> from ezcode import DoublyLinkedList
>>> l = DoublyLinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> l.print()
None <─ (T) 0 <─> 1 <─> 2 <─> 3 <─> 4 <─> 5 <─> 6 <─> 7 <─> 8 <─> 9 (H) ─> None
>>> l.copy().reverse().print()
None <─ (T) 9 <─> 8 <─> 7 <─> 6 <─> 5 <─> 4 <─> 3 <─> 2 <─> 1 <─> 0 (H) ─> None
>>> l.copy().reverse(start=2).print()
None <─ (T) 0 <─> 1 <─> 9 <─> 8 <─> 7 <─> 6 <─> 5 <─> 4 <─> 3 <─> 2 (H) ─> None
>>> l.copy().reverse(end=-3).print()
None <─ (T) 7 <─> 6 <─> 5 <─> 4 <─> 3 <─> 2 <─> 1 <─> 0 <─> 8 <─> 9 (H) ─> None
>>> l.copy().reverse(start=5, end=8).print()
None <─ (T) 0 <─> 1 <─> 2 <─> 3 <─> 4 <─> 8 <─> 7 <─> 6 <─> 5 <─> 9 (H) ─> None
>>> l.copy().reverse(start=1, end=8, group_size=3, remainder_on_left=True).print()
None <─ (T) 0 <─> 2 <─> 1 <─> 5 <─> 4 <─> 3 <─> 8 <─> 7 <─> 6 <─> 9 (H) ─> None
>>> l.copy().reverse(start=1, end=8, group_size=3, remainder_on_left=False).print()
None <─ (T) 0 <─> 3 <─> 2 <─> 1 <─> 6 <─> 5 <─> 4 <─> 8 <─> 7 <─> 9 (H) ─> None
```