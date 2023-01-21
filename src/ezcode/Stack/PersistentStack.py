from __future__ import annotations
from collections import deque


class PersistentStack:
    def __init__(self, size: int = 0, data=None, predecessor: PersistentStack = None):
        self.data = data
        self.size = size
        self.predecessor = predecessor

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self)) + "]"

    def __iter__(self) -> iter:
        predecessor, queue = self.predecessor, deque()
        if self.size > 0:
            queue.appendleft(self.data)
        for _ in range(self.size - 1):
            queue.appendleft(predecessor.data)
            predecessor = predecessor.predecessor
        return iter(queue)

    def __len__(self) -> int:
        return self.size

    def push(self, data) -> PersistentStack:
        """ O(1) """
        return PersistentStack(self.size + 1, data, self)

    def pop(self) -> PersistentStack:
        """ O(1) """
        if self.size == 0:
            raise IndexError("Pop from empty stack")
        return self.predecessor

    def top(self, k: int = 1, always_return_list: bool = False):
        """ O(k) """
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.data] if always_return_list else self.data
        else:
            predecessor, output = self.predecessor, list()
            if self.size > 0:
                output.append(self.data)
            for _ in range(k - 1):
                output.append(predecessor.data)
                predecessor = predecessor.predecessor
            return output

