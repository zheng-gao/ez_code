## Binary Search
```python
>>> from ezcode.array.search import binary_search_range
>>> class X:
...     def __init__(self, number, string):
...         self.number, self.string = number, string
... 
>>> array = [X(1,"c"), X(2,"b"), X(2,"b"), X(3,"a")]
>>> binary_search_range(target=2, array=array, is_ascending=True, is_inclusive=True, key=lambda x: x.number)
(1, 2)
>>> binary_search_range(target="b", array=array, is_ascending=False, is_inclusive=False, key=lambda x: x.string)
(0, 3)
```

## Longest Common Subsequence

```python
>>> from ezcode.array.lcs import longest_common_subsequence
>>> print(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))
['B', 'C', 'B', 'A']
```

## Longest Common Subarray

```python
>>> from ezcode.array.lcs import longest_common_subarray
>>> print(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))
['A', 'B']
```

## Split & Chunk Array

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

## Sort

### Quick Sort
```python
>>> from ezcode.array.sort import quick_sort
>>> data  = [7, 2, 4, 6, 5, 4, 1, 3, 8, 0, 6, 9, 4]
>>> quick_sort(data)
>>> print(data)
[0, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 9]
>>> data = [7, 2, 4, 6, 5, 4, 1, 3, 8, 0, 6, 9, 4]
>>> quick_sort(data, reverse=True)
>>> print(data)
[9, 8, 7, 6, 6, 5, 4, 4, 4, 3, 2, 1, 0]
```
