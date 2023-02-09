# from collections.abc import MutableSequence
from typing import Iterable

from ezcode.List.LinkedList import LinkedList


class Stack:
    def __init__(self, init_data: Iterable = None):
        self.list = LinkedList(init_data=init_data)

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return self.list.to_string(reverse=True, include_end=False, mark_head=True)

    def print(self):
        print(self)

    def push(self, data):
        self.list.append(data)

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty stack")
        return self.list.pop()

    def top(self, k: int = 1, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.list[-1]] if always_return_list else self.list[-1]
        else:
            node, output = self.list.head, list()
            for _ in range(k):
                output.append(self.list.get_data(node))
                node = self.list.get_next(node)
            return output


