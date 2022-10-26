from __future__ import annotations
from typing import Callable


class Interval:
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True, data=None):
        if start > end:
            raise ValueError(f"start \"{start}\" > end \"{end}\"")
        self.data = data
        self.start = start
        self.end = end
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

    def __str__(self):
        return f"{'[' if self.start_inclusive else '('}{self.start}, {self.end}{']' if self.end_inclusive else ')'} {self.data}"

    def __eq__(self, other: Interval) -> bool:
        return self.data == other.data and self.start == other.start and self.end == other.end and \
            self.start_inclusive == other.start_inclusive and self.end_inclusive == other.end_inclusive

    def overlaps_with(self, other: Interval) -> bool:
        # non-overlaps: [self.start, self.end] ... [other.start, other.end] ... [self.start, self.end]
        if self.start_inclusive and self.end_inclusive and other.start_inclusive and other.end_inclusive:
            return self.start <= other.end and other.start <= self.end
        elif self.start_inclusive and other.end_inclusive:
            return self.start <= other.end and other.start < self.end
        elif self.end_inclusive and other.start_inclusive:
            return self.start < other.end and other.start <= self.end
        else:
            return self.start < other.end and other.start < self.end
        """
        from ezcode.bit import bool_list_to_number
        boundary = bool_list_to_number([self.start_inclusive, self.end_inclusive, other.start_inclusive, other.end_inclusive])
        match boundary:
            case 0:   # 0000
            case 1:   # 0001
            case 2:   # 0010
            case 3:   # 0011
            case 4:   # 0100
            case 5:   # 0101
            case 8:   # 1000
            case 10:  # 1010
            case 12:  # 1100
                return self.start < other.end and other.start < self.end
            case 6:   # 0110
            case 7:   # 0111
            case 14:  # 1110
                return self.start < other.end and other.start <= self.end
            case 9:   # 1001
            case 11:  # 1011
            case 13:  # 1101
                return self.start <= other.end and other.start < self.end
            case 15:  1111     # all inclusive
                return self.start <= other.end and other.start <= self.end
            case _:
                raise ValueError(f"Wrong boundary: {boundary}")
        """

    def merge(self, other: Interval, merge_data: Callable = None) -> Interval:
        # min(starts), max(ends)
        if self.overlaps_with(other):
            if self.start < other.start:
                start = self.start
                start_inclusive = self.start_inclusive
            elif other.start < self.start:
                start = other.start
                start_inclusive = other.start_inclusive
            else:
                start = self.start
                start_inclusive = self.start_inclusive | other.start_inclusive
            if other.end < self.end:
                end = self.end
                end_inclusive = self.end_inclusive
            elif self.end < other.end:
                end = other.end
                end_inclusive = other.end_inclusive
            else:
                end = self.end
                end_inclusive = self.end_inclusive | other.end_inclusive
            data = merge_data(self.data, other.data) if merge_data else None
            return Interval(start, end, start_inclusive, end_inclusive, data)
        return None

    def intersect(self, other: Interval, intersect_data: Callable = None) -> Interval:
        # max(starts), min(ends)
        if self.overlaps_with(other):
            if self.start < other.start:
                start = other.start
                start_inclusive = other.start_inclusive
            elif other.start < self.start:
                start = self.start
                start_inclusive = self.start_inclusive
            else:
                start = self.start
                start_inclusive = self.start_inclusive & other.start_inclusive
            if other.end < self.end:
                end = other.end
                end_inclusive = other.end_inclusive
            elif self.end < other.end:
                end = self.end
                end_inclusive = self.end_inclusive
            else:
                end = self.end
                end_inclusive = self.end_inclusive & other.end_inclusive
            data = intersect_data(self.data, other.data) if intersect_data else None
            return Interval(start, end, start_inclusive, end_inclusive, data)
        return None









