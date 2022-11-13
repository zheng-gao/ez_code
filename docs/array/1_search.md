# Binary Search
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