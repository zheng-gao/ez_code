# Tailed Linked List
## Overview

[ezcode.List](../../src/ezcode/List/__init__.py).[TailedLinkedList](../../src/ezcode/List/TailedLinkedList.py#L9) inherits from [ezcode.List.LinkedList](../../src/ezcode/List/LinkedList.py#L10). It maintains a tail pointer to the first node and a head pointer to the last node. New nodes can be appended from both sides, but nodes can only be poped from head. So it can be used as both Queue (FIFO) and Stack (LIFO)  

## Details
### Iterator
```python
>>> from ezcode import TailedLinkedList
>>> l = TailedLinkedList([0, 1, 2, 3])
>>> list(iter(l))
[0, 1, 2, 3]
>>> list(reversed(l))
[3, 2, 1, 0]
```
### Append, Append Left & Pop
```python
>>> from ezcode import TailedLinkedList
>>> l = TailedLinkedList()
>>> for i in range(3):
...     l.append(i)
... 
>>> for i in range(3, 6):
...     l.appendleft(i)
... 
>>> l.print()
None <─ (T) 5 <─ 4 <─ 3 <─ 0 <─ 1 <─ 2 (H)
>>> while len(l) > 0:
...     print(l.pop(), end=" ")
... 
2 1 0 3 4 5
```
### Reverse & Copy
```python
>>> from ezcode import TailedLinkedList
>>> l = TailedLinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> l.print()
None <─ (T) 0 <─ 1 <─ 2 <─ 3 <─ 4 <─ 5 <─ 6 <─ 7 <─ 8 <─ 9 (H)
>>> l.copy().reverse().print()
None <─ (T) 9 <─ 8 <─ 7 <─ 6 <─ 5 <─ 4 <─ 3 <─ 2 <─ 1 <─ 0 (H)
>>> l.copy().reverse(start=2).print()
None <─ (T) 0 <─ 1 <─ 9 <─ 8 <─ 7 <─ 6 <─ 5 <─ 4 <─ 3 <─ 2 (H)
>>> l.copy().reverse(end=-3).print()
None <─ (T) 7 <─ 6 <─ 5 <─ 4 <─ 3 <─ 2 <─ 1 <─ 0 <─ 8 <─ 9 (H)
>>> l.copy().reverse(start=5, end=8).print()
None <─ (T) 0 <─ 1 <─ 2 <─ 3 <─ 4 <─ 8 <─ 7 <─ 6 <─ 5 <─ 9 (H)
>>> l.copy().reverse(start=1, end=8, group_size=3, remainder_on_left=True).print()
None <─ (T) 0 <─ 2 <─ 1 <─ 5 <─ 4 <─ 3 <─ 8 <─ 7 <─ 6 <─ 9 (H)
>>> l.copy().reverse(start=1, end=8, group_size=3, remainder_on_left=False).print()
None <─ (T) 0 <─ 3 <─ 2 <─ 1 <─ 6 <─ 5 <─ 4 <─ 8 <─ 7 <─ 9 (H)
```