# Interval
## overlap
```python
>>> from ezcode.interval import Interval
>>> Interval(1, 5).overlap(Interval(3, 6))
True
>>> Interval(1, 2).overlap(Interval(3, 6))
False
>>> Interval(1, 5).overlap(Interval(3, 4))
True
>>> Interval(1, 3).overlap(Interval(3, 5))
True
>>> Interval(1, 3, right_open=True).overlap(Interval(3, 5))
False
```
## merge
```python
>>> print(Interval(1, 2).merge(Interval(2, 3, left_open=True)))
None
>>> Interval(1, 2, data=100).merge(Interval(2, 3, data=200), merge_data=lambda x,y: x+y)
Interval(1, 3, data=300)
```
## intersect
```python
>>> print(Interval(1, 2).intersect(Interval(2, 3, left_open=True)))
None
>>> Interval(1, 2, data=100).intersect(Interval(2, 3, data=200), intersect_data=min)
Interval(2, 2, data=100)
```
## merge_intervals
```python
>>> from ezcode.interval import Interval
>>> from ezcode.interval.algorithm import merge_intervals
>>> merge_intervals([Interval(3, 4), Interval(1, 2), Interval(2, 5),Interval(7, 9), Interval(8, 9), Interval(6, 8)])
[Interval(1, 5), Interval(6, 9)]
```
## overlapping_interval_pairs
```python
>>> from ezcode.interval import Interval
>>> from ezcode.interval.algorithm import overlapping_interval_pairs
>>> pairs = overlapping_interval_pairs([Interval(1, 2), Interval(2, 3), Interval(3, 4)])
>>> for p in pairs:
...     print(p)
... 
(Interval(1, 2), Interval(2, 3))
(Interval(2, 3), Interval(3, 4))
```
## min_groups_of_non_overlapping_intervals
```python
>>> from ezcode.interval import Interval
>>> from ezcode.interval.algorithm import min_groups_of_non_overlapping_intervals
>>> intervals = [Interval(3, 4), Interval(1, 2), Interval(2, 5), Interval(7, 9), Interval(8, 9), Interval(6, 8)]
>>> groups = min_groups_of_non_overlapping_intervals(intervals)
>>> for group in groups:
...     print(group)
... 
[Interval(1, 2), Interval(3, 4), Interval(6, 8)]
[Interval(2, 5), Interval(7, 9)]
[Interval(8, 9)]
```
## most_overlapped_subintervals
```python
>>> from ezcode.interval.algorithm import most_overlapped_subintervals
>>> most_overlapped_subintervals([(0, 10), (5, 12), (8, 13), (11, 12)])
(3, [(8, 10), (11, 12)])

>>> data = [
...     (1920, 1954),
...     (1931, 1975),
...     (1921, 1922),
...     (1992, 2007),
...     (1953, 2017),
...     (1700, 1722),
...     (2016, 2017),
...     (1930, 2001),
...     (1990, 2011),
...     (1967, 2019),
...     (1905, 1987),
...     (1990, 2018),
...     (1998, 2015),
...     (1993, 2019)
... ]
>>> most_overlapped_subintervals(data)
(8, [(1998, 2001)])
```
