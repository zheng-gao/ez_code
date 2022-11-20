# Persistent Stack
```python
>>> from ezcode.list.stack import PersistentStack
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
...     print(f"{len(s)}: {s}")
... 
0: []
1: [1]
2: [1, 2]
3: [1, 2, 3]
2: [1, 2]
3: [1, 2, 4]
4: [1, 2, 4, 5]
3: [1, 2, 4]
4: [1, 2, 4, 6]
3: [1, 2, 4]
2: [1, 2]
3: [1, 2, 7]
2: [1, 2]
1: [1]
0: []
```
