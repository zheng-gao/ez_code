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

## RandomKeyValueDictionary
```python
>>> from collections import Counter
>>> from ezcode.random import RandomKeyValueDictionary
>>> key_counter, value_counter = Counter(), Counter()
>>> rkv_dict = RandomKeyValueDictionary({'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard', 'A': 'upper', 'c': 'lower'})
>>> for _ in range(600):
...     key_counter.update([rkv_dict.random_key()])
...     value_counter.update([rkv_dict.random_value()])
... 
>>> print(key_counter)
Counter({'c': 109, '*': 108, 'a': 107, '!': 96, 'A': 95, 'b': 85})
>>> print(value_counter)
Counter({'lower': 297, 'punctuation': 110, 'wildcard': 100, 'upper': 93})
```

## RandomUniqueValueDictionary
```Python
>>> from collections import Counter
>>> from ezcode.random import RandomUniqueValueDictionary
>>> value_counter = Counter()
>>> rkv_dict = RandomUniqueValueDictionary({'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard', 'A': 'upper', 'c': 'lower'})
>>> for _ in range(400):
...     value_counter.update([rkv_dict.random_value()])
... 
>>> print(value_counter)
Counter({'upper': 107, 'punctuation': 102, 'lower': 99, 'wildcard': 92})
```