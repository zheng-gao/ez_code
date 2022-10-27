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
>>> overlapping_interval_pairs([Interval(1, 2), Interval(2, 3), Interval(3, 4)])
[(Interval(1, 2), Interval(2, 3)), (Interval(2, 3), Interval(3, 4))]
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
