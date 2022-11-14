from __future__ import annotations
from collections import deque


class PStack:
    class Node:
        def __init__(self, value, predecessor: PStack.Node = None):
            self.value = value
            self.predecessor = predecessor

        def __str__(self):
            return str(self.value)

    def __init__(self, size: int = 0, top: PStack.Node = None):
        self.size = size
        self.top = top

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self)) + "]"

    def __iter__(self) -> iter:
        node, values = self.top, deque()
        while node:
            values.appendleft(node.value)
            node = node.predecessor
        return iter(values)

    def __len__(self) -> int:
        return self.size

    def push(self, value) -> PStack:
        if self.size == 0:
            return PStack(1, self.Node(value, None))
        return PStack(self.size + 1, self.Node(value, self.top))

    def pop(self) -> PStack:
        if self.size == 0:
            raise IndexError("Pop Empty PStack")
        return PStack(self.size - 1, self.top.predecessor)
