# Persistent Stack
```python
>>> from ezcode.stack import PersistentStack
>>> stacks = [PersistentStack()]
>>> stacks.append(stacks[-1].push(1))
>>> stacks.append(stacks[-1].push(2))
>>> stacks.append(stacks[-1].push(3))
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].push(4))
>>> stacks.append(stacks[-1].push(5))
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].push(6))
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].push(7))
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].pop())
>>> stacks.append(stacks[-1].pop())
>>> for s in stacks:
...     print(f"size {len(s)}: {s}")
... 
size 0: []
size 1: [1]
size 2: [1, 2]
size 3: [1, 2, 3]
size 2: [1, 2]
size 3: [1, 2, 4]
size 4: [1, 2, 4, 5]
size 3: [1, 2, 4]
size 4: [1, 2, 4, 6]
size 3: [1, 2, 4]
size 2: [1, 2]
size 3: [1, 2, 7]
size 2: [1, 2]
size 1: [1]
size 0: []
```
