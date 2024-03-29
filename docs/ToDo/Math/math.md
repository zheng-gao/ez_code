# Permutations

```python
>>> from ezcode.array.utils import print_array
>>> from ezcode.math.discrete import permutations
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

>>> from ezcode.math.discrete import next_lexicographic_permutation
>>> next_lexicographic_permutation(['A', 'A', 'B'])
['A', 'B', 'A']
```

# Combinations

```python
>>> from ezcode.array.utils import print_array
>>> from ezcode.math.discrete import combinations, all_subsets
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

# Partitions

```python
>>> from ezcode.array.utils import print_array
>>> from ezcode.math.discrete import partitions
>>> print_array(partitions([1, 2, 3, 4]))
[
    [
        [1, 2, 3, 4],
    ],
    [
        [1],
        [2, 3, 4],
    ],
    [
        [1],
        [2],
        [3, 4],
    ],
    [
        [1],
        [2],
        [3],
        [4],
    ],
    [
        [1],
        [2, 3],
        [4],
    ],
    [
        [1, 2],
        [3, 4],
    ],
    [
        [1, 2],
        [3],
        [4],
    ],
    [
        [1, 2, 3],
        [4],
    ],
]
```

# Enumerations

```python
>>> from ezcode.array.utils import print_array
>>> from ezcode.math.discrete import enumerations
>>> print_array(enumerations([['a', 'b'], ['X', 'Y'], [1, 2, 3]]))
[
    [a, X, 1],
    [a, X, 2],
    [a, X, 3],
    [a, Y, 1],
    [a, Y, 2],
    [a, Y, 3],
    [b, X, 1],
    [b, X, 2],
    [b, X, 3],
    [b, Y, 1],
    [b, Y, 2],
    [b, Y, 3],
]
```

# Calculator
```python
>>> from ezcode.math.calculator import infix_notation_to_reverse_polish_notation
>>> from ezcode.math.calculator import evaluate_reverse_polish_notation
>>> from ezcode.math.calculator import calculate
>>> arithmetic_expression = "-2/-1 + √4! * ((-1 + 5)-2)/2"
>>> rpn = infix_notation_to_reverse_polish_notation(arithmetic_expression)
>>> print(rpn)
[-2, -1, '/', 4, '!', '√', -1, 5, '+', 2, '-', '*', 2, '/', '+']

>>> evaluate_reverse_polish_notation(rpn)
6.898979485566356

>>> calculate(arithmetic_expression)
6.898979485566356
```
