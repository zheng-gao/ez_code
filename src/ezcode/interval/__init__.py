from __future__ import annotations
from typing import Callable


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

    def __str__(self):
        return f"{'(' if self.left_open else '['}{self.left}, {self.right}{')' if self.right_open else ']'}: {self.data}"

    def __eq__(self, other: Interval) -> bool:
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

