# String

## rotate_char
```python
"""
rotate_factor = 1
'0' -> '1' -> ... -> '9' -> '0' -> ...
'a' -> 'b' -> ... -> 'z' -> 'a' -> ...
'A' -> 'B' -> ... -> 'Z' -> 'A' -> ...
rotate_factor = -2
'0' -> '8' -> '6' -> ... -> '2' -> '0' -> ...
'a' -> 'y' -> 'w' -> ... -> 'c' -> 'a' -> ...
'A' -> 'Y' -> 'W' -> ... -> 'C' -> 'A' -> ...
"""
>>> from ezcode.string import rotate_char
>>> rotate_char('x', 5)
'c'
>>> rotate_char('3', -5)
'8'
>>> rotate_char('E', -5)
'Z'
```

## substrings
```python
>>> from ezcode.string import substrings
>>> substrings("abbbc", unique=True, by_size=False)
['a', 'b', 'c', 'ab', 'bb', 'bc', 'abb', 'bbb', 'bbc', 'abbb', 'bbbc', 'abbbc']
>>> substrings("abbbc", unique=True, by_size=True)
{
    1: ['a', 'b', 'c'],
    2: ['ab', 'bb', 'bc'],
    3: ['abb', 'bbb', 'bbc'],
    4: ['abbb', 'bbbc'],
    5: ['abbbc']
}
```
