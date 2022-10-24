from collections import deque
from ezcode.heap import PriorityQueue


def overlapped(interval_1: tuple, interval_2: tuple, is_inclusive: bool = True) -> bool:
    if is_inclusive:
        return interval_1[0] <= interval_2[1] and interval_2[0] <= interval_1[1]
    else:
        return interval_1[0] < interval_2[1] and interval_2[0] < interval_1[1]


def intersect(interval_1: tuple, interval_2: tuple, is_inclusive: bool = True) -> tuple:
    if overlapped(interval_1, interval_2, is_inclusive):
        return max(interval_1[0], interval_2[0]), min(interval_1[1], interval_2[1])
    return None


def merge(interval_1: tuple, interval_2: tuple, is_inclusive: bool = True) -> tuple:
    if overlapped(interval_1, interval_2, is_inclusive):
        return min(interval_1[0], interval_2[0]), max(interval_1[1], interval_2[1])
    return None


def merge_all(intervals: list[tuple], is_inclusive: bool = True) -> list[tuple]:
    if not intervals:
        return list()
    intervals.sort(key=lambda x: x[0])
    merged, output = intervals[0], list()
    for interval in intervals[1:]:
        tmp = merge(merged, interval, is_inclusive)
        if tmp is None:  # non-overlapping
            output.append(merged)
            merged = interval
        else:
            merged = tmp
    output.append(merged)
    return output


def all_overlapped_pairs(intervals: list[tuple], is_inclusive: bool = True) -> list[list[tuple]]:
    intervals.sort(key=lambda x: x[0])
    circular_queue, output = deque(), list()
    for interval in intervals:
        for _ in range(len(circular_queue)):
            interval_tmp = circular_queue.popleft()
            if overlapped(interval_tmp, interval, is_inclusive):
                circular_queue.append(interval_tmp)
                output.append([interval_tmp, interval])
        circular_queue.append(interval)
    return output


def min_groups_of_non_overlapped_intervals(intervals: list[tuple], is_inclusive: bool = True) -> list[list[tuple]]:
    intervals.sort(key=lambda x: x[0])
    min_queue = PriorityQueue(min_heap=True, key=lambda group: group[-1][-1])
    for interval in intervals:
        if len(min_queue) == 0:
            min_queue.push([interval])
        else:
            group = min_queue.top()
            if overlapped(group[-1], interval, is_inclusive):  # need a new group
                min_queue.push([interval])
            else:
                group.append(interval)
                min_queue.update_top(group)
    return min_queue.items(with_priority=False)


class NonOverlappedIntervals:
    def __init__(self, is_inclusive: bool = True):
        self.is_inclusive = is_inclusive
        self.intervals = deque()  # non-overlapped intervals sorted by first item

    def add_interval(self, interval: tuple):
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

    def add_intervals(self, intervals: list[tuple]):
        for interval in intervals:
            self.add_interval(interval)











