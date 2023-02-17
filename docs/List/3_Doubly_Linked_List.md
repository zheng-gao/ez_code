# Doubly Linked List
## Overview

The class [DoublyLinkedList](../../src/ezcode/List/DoublyLinkedList.py#L10) is inherited from [ezcode.List.LinkedList](../../src/ezcode/List/TailedLinkedList.py#L8)

## Examples
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
None <─ (T) 5 <─> 4 <─> 3 <─> 0 <─> 1 <─> 2 (H)
>>> while len(l) > 3:
...     print(l.pop(), end=" ")
... 
2 1 0
>>> while len(l) > 0:
...     print(l.popleft(), end=" ")
... 
5 4 3
```