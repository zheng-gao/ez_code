from collections import deque
from ezcode.heap import PriorityQueue


def overlapped(interval_1: tuple, interval_2: tuple, inclusive=True) -> bool:
    if inclusive:
        return interval_1[0] <= interval_2[1] and interval_2[0] <= interval_1[1]
    else:
        return interval_1[0] < interval_2[1] and interval_2[0] < interval_1[1]


def intersect(interval_1: tuple, interval_2: tuple, inclusive=True) -> tuple:
    if overlapped(interval_1, interval_2, inclusive):
        return max(interval_1[0], interval_2[0]), min(interval_1[1], interval_2[1])
    return None


def merge(interval_1: tuple, interval_2: tuple, inclusive=True) -> tuple:
    if overlapped(interval_1, interval_2, inclusive):
        return min(interval_1[0], interval_2[0]), max(interval_1[1], interval_2[1])
    return None


def merge_all(intervals: list[tuple], inclusive=True) -> list[tuple]:
    if not intervals:
        return list()
    intervals.sort(key=lambda x: x[0])
    merged, output = intervals[0], list()
    for interval in intervals[1:]:
        tmp = merge(merged, interval, inclusive)
        if tmp is None:  # non-overlapping
            output.append(merged)
            merged = interval
        else:
            merged = tmp
    output.append(merged)
    return output


def all_overlapped_pairs(intervals: list[tuple], inclusive=True) -> list[list[tuple]]:
    intervals.sort(key=lambda x: x[0])
    circular_queue, output = deque(), list()
    for interval in intervals:
        for _ in range(len(circular_queue)):
            interval_tmp = circular_queue.popleft()
            if overlapped(interval_tmp, interval, inclusive):
                circular_queue.append(interval_tmp)
                output.append([interval_tmp, interval])
        circular_queue.append(interval)
    return output


def min_groups_of_non_overlapped_intervals(intervals: list[tuple], inclusive=True) -> list[list[tuple]]:
    intervals.sort(key=lambda x: x[0])
    priority_queue = PriorityQueue(min_heap=True)
    for interval in intervals:
        if len(priority_queue) == 0:
            priority_queue.push(interval[1], [interval])
        else:
            group = priority_queue.peek()[1]
            if overlapped(group[-1], interval, inclusive):
                priority_queue.push(interval[1], [interval])
            else:
                group.append(interval)
                priority_queue.update_top(interval[1])
    return [group for _, group in priority_queue.heap]


