from __future__ import annotations
from collections import deque
from functools import cmp_to_key
from typing import Callable

from ezcode.Heap.PriorityQueue import PriorityQueue
from ezcode.Heap.PriorityMap import PriorityMap


class Interval:
    def __init__(self, left, right, left_open: bool = False, right_open: bool = False, data=None):
        self.data = data
        self.left = left
        self.right = right
        self.left_open = left_open
        self.right_open = right_open
        if left < right:
            self.is_empty = False
        elif left > right:
            self.is_empty = True
        else:
            self.is_empty = left_open or right_open

    def __repr__(self):
        string = f"{type(self).__name__}({self.left}, {self.right}"
        if self.left_open:
            string += ", left_open=True"
        if self.right_open:
            string += ", right_open=True"
        if self.data is not None:
            string += f", data={self.data}"
        return string + ")"

    def equal(self, other: Interval) -> bool:
        if self.is_empty and other.is_empty:
            return self.data == other.data
        elif not self.is_empty and not other.is_empty:
            return self.data == other.data and \
                self.left == other.left and self.right == other.right and \
                self.left_open == other.left_open and self.right_open == other.right_open
        else:
            return False

    def overlap(self, other: Interval) -> bool:
        """ exist non-empty common subset """
        if self.is_empty or other.is_empty:
            return False
        if not self.left_open and not self.right_open and not other.left_open and not other.right_open:
            return self.left <= other.right and other.left <= self.right
        elif not self.left_open and not other.right_open:
            return self.left <= other.right and other.left < self.right
        elif not self.right_open and not other.left_open:
            return self.left < other.right and other.left <= self.right
        else:
            return self.left < other.right and other.left < self.right

    def merge(self, other: Interval, merge_data: Callable = None) -> Interval:
        """ union if overlapping """
        if self.overlap(other):
            if self.left < other.left:
                left = self.left
                left_open = self.left_open
            elif other.left < self.left:
                left = other.left
                left_open = other.left_open
            else:
                left = self.left
                left_open = self.left_open and other.left_open
            if other.right < self.right:
                right = self.right
                right_open = self.right_open
            elif self.right < other.right:
                right = other.right
                right_open = other.right_open
            else:
                right = self.right
                right_open = self.right_open and other.right_open
            data = merge_data(self.data, other.data) if merge_data else None
            return Interval(left, right, left_open, right_open, data)
        return None

    def intersect(self, other: Interval, intersect_data: Callable = None) -> Interval:
        """ largest non-empty common subset """
        if self.overlap(other):
            if self.left < other.left:
                left = other.left
                left_open = other.left_open
            elif other.left < self.left:
                left = self.left
                left_open = self.left_open
            else:
                left = self.left
                left_open = self.left_open or other.left_open
            if other.right < self.right:
                right = other.right
                right_open = other.right_open
            elif self.right < other.right:
                right = self.right
                right_open = self.right_open
            else:
                right = self.right
                right_open = self.right_open or other.right_open
            data = intersect_data(self.data, other.data) if intersect_data else None
            return Interval(left, right, left_open, right_open, data)
        return None


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
    circular_queue, output = deque(), list()  # every pair only visit once, O(P) where P is the number of pairs
    for interval in sorted(intervals, key=lambda interval: interval.left):  # sort = O(NlogN) < P ~ N^2
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
    """ buildings = [(left, right, height), (...), ...] -> [(position, height), ...] """
    output, l_map, r_map = list(), dict(), dict()
    for left, right, height in buildings:
        interval = Interval(left, right, data=height)
        if left not in l_map:
            l_map[left] = list()
        l_map[left].append(interval)
        if right not in r_map:
            r_map[right] = list()
        r_map[right].append(interval)
    index_l, index_r, sorted_l, sorted_r = 0, 0, sorted(l_map.keys()), sorted(r_map.keys())
    max_map = PriorityMap(min_heap=False, key=lambda interval: interval.data)
    while index_r < len(sorted_r):
        left, right = sorted_l[index_l] if index_l < len(sorted_l) else float("inf"), sorted_r[index_r]
        if left >= right:  # process right edge first
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


def most_overlapped_subintervals(intervals: list[tuple]) -> tuple[int, list[tuple]]:
    """
    only support inclusive/close boundary
    return: depth, list(intervals)
    """
    events = list()
    for left, right in intervals:
        events.append((left, True))  # is_left = True
        events.append((right, False))  # is_left = False

    def compare_event(event_1, event_2):
        if event_1[0] == event_2[0]:
            return -1 if event_1[1] else 1  # left side first
        else:
            return event_1[0] - event_2[0]

    events.sort(key=cmp_to_key(compare_event))  # O(2N*log2N) ~ O(NlogN)
    deepest_intervals, deepest_left, max_depth, depth = list(), None, 0, 0
    for boundary, is_left in events:
        if is_left:
            depth += 1
            if depth > max_depth:
                max_depth = depth
                deepest_left = boundary
                deepest_intervals.clear()
            elif depth == max_depth:
                deepest_left = boundary
        else:
            if depth == max_depth:
                deepest_intervals.append((deepest_left, boundary))
            depth -= 1
    return max_depth, deepest_intervals


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

