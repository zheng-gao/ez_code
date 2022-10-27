from collections import deque
from typing import Callable

from ezcode.heap import PriorityQueue, PriorityMap
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


def skyline(buildings: list[tuple]) -> list[tuple]:
    output, l_map, r_map = list(), dict(), dict()
    for left, right, height in buildings:
        interval = Interval(left, right, data=height)
        if left not in l_map:
            l_map[left] = list()
        l_map[left].append(interval)
        if right not in r_map:
            r_map[right] = list()
        r_map[right].append(interval)
    index_l, sorted_l, index_r, sorted_r = 0, sorted(l_map.keys()), 0, sorted(r_map.keys())
    max_map = PriorityMap(min_heap=False, key=lambda interval: interval.data)
    while index_r < len(sorted_r):
        left, right = sorted_l[index_l] if index_l < len(sorted_l) else float("inf"), sorted_r[index_r]
        if left >= right:
            for interval in r_map[right]:
                del max_map[interval]
            if left != right:
                height = 0 if max_map.is_empty() else max_map.top().data
                if output[-1][1] != height:
                    output.append((right, height))
            index_r += 1
        if left <= right:
            for interval in l_map[left]:
                max_map.push(interval)
            height = max_map.top().data
            if len(output) == 0 or output[-1][1] != height:
                output.append((left, height))
            index_l += 1
    return output


"""
class NonOverlappingIntervals:

    keep sorted, use binary search for add or use treemap to store intervals

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

