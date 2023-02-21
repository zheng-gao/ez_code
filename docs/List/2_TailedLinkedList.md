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