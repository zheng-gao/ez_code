## RandomMultiSet
```python
>>> from collections import Counter
>>> from ezcode.random import RandomMultiSet
>>> counter = Counter()
>>> rm_set = RandomMultiSet(["a", "a", "b", "a"])
>>> for _ in range(400):
...     counter.update([rm_set.random()])
... 
>>> print(counter)
Counter({'a': 303, 'b': 97})
```

## RandomKeyValueDict & RandomUniqueValueDict
```python
>>> from collections import Counter
>>> from ezcode.random import RandomKeyValueDict, RandomUniqueValueDict
>>> key_counter, value_counter = Counter(), Counter()
>>> data = {
...     'a': 'lower',
...     'b': 'lower',
...     'c': 'lower',
...     'A': 'upper',
...     '*': 'wildcard',
...     '!': 'punctuation'
... }
>>> rkv_dict = RandomKeyValueDict(data)
>>> for _ in range(600):
...     key_counter.update([rkv_dict.random_key()])
...     value_counter.update([rkv_dict.random_value()])
... 
>>> print(key_counter)
Counter({'a': 107, '!': 102, '*': 100, 'c': 99, 'b': 97, 'A': 95})
>>> print(value_counter)
Counter({'lower': 305, 'punctuation': 104, 'wildcard': 102, 'upper': 89})
>>> value_counter = Counter()
>>> ruv_dict = RandomUniqueValueDict(data)
>>> for _ in range(400):
...     value_counter.update([ruv_dict.random_value()])
... 
>>> print(value_counter)
Counter({'lower': 105, 'upper': 101, 'wildcard': 99, 'punctuation': 95})
```

## RandomWeightedIndex
```python
>>> from collections import Counter
>>> from ezcode.random import RandomWeightedIndex
>>> counter = Counter()
>>> rwi = RandomWeightedIndex([1, 2, 3, 4])
>>> for _ in range(1000):
...     counter.update([rwi.random_index()])
... 
>>> print(counter)
Counter({3: 403, 2: 303, 1: 187, 0: 107})
```