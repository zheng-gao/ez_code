from collections import deque
from typing import Callable

from ezcode.heap import PriorityQueue
from ezcode.interval import Interval


def merge_intervals(intervals: list[Interval], merge_data: Callable = None) -> list[Interval]:
    merged, output = None, list()
    for interval in sorted(intervals, key=lambda interval: interval.left):
        if interval.is_empty:
            output.append(interval)
        elif merged is None:
            merged = interval
        else:
            tmp = merged.merge(interval, merge_data)
            if tmp is None:  # non-overlapping
                output.append(merged)
                merged = interval
            else:
                merged = tmp
    if merged is not None:
        output.append(merged)
    return output


def overlapping_interval_pairs(intervals: list[Interval]) -> list[tuple[Interval, Interval]]:
    circular_queue, output = deque(), list()
    for interval in sorted(intervals, key=lambda interval: interval.left):
        if not interval.is_empty:
            for _ in range(len(circular_queue)):
                tmp = circular_queue.popleft()
                if tmp.overlap(interval):  # if not overlap, any latter interval doesn't overlap either
                    circular_queue.append(tmp)
                    output.append((tmp, interval))
            circular_queue.append(interval)
    return output


def min_groups_of_non_overlapping_intervals(intervals: list[Interval]) -> list[list[Interval]]:
    min_queue = PriorityQueue(min_heap=True, key=lambda group: group[-1].right)
    for interval in sorted(intervals, key=lambda interval: interval.left):
        if min_queue.is_empty():
            min_queue.push([interval])
        else:
            group = min_queue.top()
            if group[-1].overlap(interval):  # need a new group
                min_queue.push([interval])
            else:
                group.append(interval)
                min_queue.update_top(group)
    return min_queue.items(with_priority=False)


"""
class NonOverlappingIntervals:
    def __init__(self):
        self.intervals = deque()  # non-overlapped intervals sorted by first item

    def add_interval(self, interval: Interval):
        for _ in range(len(self.intervals)):
            tmp = self.intervals.popleft()
            if interval is None:
                self.intervals.append(tmp)
            else:
                merged = merge(tmp, interval, self.is_inclusive)
                if merged is None:
                    if interval[0] < tmp[0]:
                        self.intervals.append(interval)
                        interval = None
                    self.intervals.append(tmp)
                else:
                    interval = merged
        if interval is not None:
            self.intervals.append(interval)

    def add_intervals(self, intervals: list[Interval]):
        for interval in intervals:
            self.add_interval(interval)

    def test_non_overlapped_intervals(intervals, benchmark):
        non_overlapped_intervals = NonOverlappedIntervals()
        non_overlapped_intervals.add_intervals(intervals)
        assert list(non_overlapped_intervals.intervals) == benchmark

    test_non_overlapped_intervals(intervals=[(2, 3), (6, 8), (0, 1)], benchmark=[(0, 1), (2, 3), (6, 8)])
    test_non_overlapped_intervals(intervals=[(1, 3), (6, 8), (0, 2)], benchmark=[(0, 3), (6, 8)])
    test_non_overlapped_intervals(intervals=[(1, 3), (6, 8), (2, 4)], benchmark=[(1, 4), (6, 8)])
    test_non_overlapped_intervals(intervals=[(1, 2), (6, 8), (3, 5)], benchmark=[(1, 2), (3, 5), (6, 8)])
    test_non_overlapped_intervals(intervals=[(1, 3), (5, 8), (2, 6)], benchmark=[(1, 8)])
    test_non_overlapped_intervals(intervals=[(1, 2), (6, 8), (5, 7)], benchmark=[(1, 2), (5, 8)])
    test_non_overlapped_intervals(intervals=[(1, 3), (5, 8), (7, 9)], benchmark=[(1, 3), (5, 9)])
    test_non_overlapped_intervals(intervals=[(1, 3), (5, 6), (7, 9)], benchmark=[(1, 3), (5, 6), (7, 9)])

"""

