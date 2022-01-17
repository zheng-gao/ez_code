# Permutations & Combinations
```
>>> from ezcode.array.utils import print_array
>>> from ezcode.math.discrete import permutations, combinations, all_subsets
>>> print_array(permutations(items=["A","A","B","B","C"], selection_size=3))
[
    ['A', 'A', 'B'],
    ['A', 'A', 'C'],
    ['A', 'B', 'A'],
    ['A', 'B', 'B'],
    ['A', 'B', 'C'],
    ['A', 'C', 'A'],
    ['A', 'C', 'B'],
    ['B', 'A', 'A'],
    ['B', 'A', 'B'],
    ['B', 'A', 'C'],
    ['B', 'B', 'A'],
    ['B', 'B', 'C'],
    ['B', 'C', 'A'],
    ['B', 'C', 'B'],
    ['C', 'A', 'A'],
    ['C', 'A', 'B'],
    ['C', 'B', 'A'],
    ['C', 'B', 'B'],
]
>>> print_array(combinations(items=["A","A","B","B","C"], selection_size=3))
[
    ['A', 'A', 'B'],
    ['A', 'A', 'C'],
    ['A', 'B', 'B'],
    ['A', 'B', 'C'],
    ['B', 'B', 'C'],
]
>>> print_array(all_subsets(items=["A","A","B","B","C"]))
[
    [],
    ['A'],
    ['B'],
    ['C'],
    ['A', 'A'],
    ['A', 'B'],
    ['A', 'C'],
    ['B', 'B'],
    ['B', 'C'],
    ['A', 'A', 'B'],
    ['A', 'A', 'C'],
    ['A', 'B', 'B'],
    ['A', 'B', 'C'],
    ['B', 'B', 'C'],
    ['A', 'A', 'B', 'B'],
    ['A', 'A', 'B', 'C'],
    ['A', 'B', 'B', 'C'],
    ['A', 'A', 'B', 'B', 'C'],
]
```