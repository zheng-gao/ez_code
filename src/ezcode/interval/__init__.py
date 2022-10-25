from __future__ import annotations
from typing import Callable


class Interval:
    def __init__(self, data, start, end, start_inclusive=True, end_inclusive=True):
        if start > end:
            raise ValueError(f"start \"{start}\" > end \"{end}\"")
        self.data = data
        self.start = start
        self.end = end
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

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
        pass
