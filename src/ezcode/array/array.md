
## Longest Common Subsequence

```
>>> from ezcode.array.lcs import longest_common_subsequence
>>> print(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))
['B', 'C', 'B', 'A']
```

## Longest Common Subarray

```
>>> from ezcode.array.lcs import longest_common_subarray
>>> print(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))
['A', 'B']
```

## Split & Chunk Array

```
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