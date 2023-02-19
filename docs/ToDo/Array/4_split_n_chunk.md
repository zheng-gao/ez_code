# Split & Chunk Array

```python
>>> from ezcode.array.utils import split_list, chunk_list, print_array
>>> l = [1, 2, 3, 4, 5]
>>> for i in l:
...     print_array(split_list(l, i))
... 
[
    [1, 2, 3, 4, 5],
]
[
    [1, 2, 3],
    [4, 5],
]
[
    [1, 2],
    [3, 4],
    [5],
]
[
    [1, 2],
    [3],
    [4],
    [5],
]
[
    [1],
    [2],
    [3],
    [4],
    [5],
]
>>> for i in l:
...     print_array(chunk_list(l, i))
... 
[
    [1],
    [2],
    [3],
    [4],
    [5],
]
[
    [1, 2],
    [3, 4],
    [5],
]
[
    [1, 2, 3],
    [4, 5],
]
[
    [1, 2, 3, 4],
    [5],
]
[
    [1, 2, 3, 4, 5],
]
```