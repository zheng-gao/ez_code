# Tailed Linked List
## Overview

The class [TailedLinkedList](../../src/ezcode/List/TailedLinkedList.py#L9) is inherited from [ezcode.List.LinkedList](../../src/ezcode/List/LinkedList.py#L10)

## Examples
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