from __future__ import annotations
from collections import deque

from ezcode.list.linked_list import SinglyLinkedList


class Stack:
    def __init__(self):
        self.singly_linked_list = SinglyLinkedList()

    def __len__(self):
        return len(self.singly_linked_list)

    def __str__(self):
        return self.singly_linked_list.to_string(reverse=True)

    def print(self):
        print(self)

    def push(self, data):
        self.singly_linked_list.add_to_head(data)

    def top(self, k: int = 1, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.singly_linked_list.peek_head()] if always_return_list else self.singly_linked_list.peek_head()
        else:
            node, output = self.singly_linked_list.head, list()
            for _ in range(k):
                output.append(self.singly_linked_list.algorithm.get_data(node))
                node = self.singly_linked_list.algorithm.get_next(node)
            return output

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty stack")
        return self.singly_linked_list.pop_head()


class MinStack:
    def __init__(self):
        self.stack = Stack()
        self.min_stack = Stack()

    def get_min(self):
        return self.min_stack.top()

    def push(self, data):
        if len(self.min_stack) == 0 or data <= self.min_stack.top():
            self.min_stack.push(data)
        self.stack.push(data)

    def top(self, k: int = 1, always_return_list: bool = False):
        return self.stack.top(k, always_return_list)

    def pop(self):
        if self.stack.top() == self.min_stack.top():
            self.min_stack.pop()
        return self.stack.pop()


class MaxStack:
    def __init__(self):
        self.stack = Stack()
        self.max_stack = Stack()

    def get_max(self):
        return self.max_stack.top()

    def push(self, data):
        if len(self.max_stack) == 0 or data >= self.max_stack.top():
            self.max_stack.push(data)
        self.stack.push(data)

    def top(self, k: int = 1, always_return_list: bool = False):
        return self.stack.top(k, always_return_list)

    def pop(self):
        if self.stack.top() == self.max_stack.top():
            self.max_stack.pop()
        return self.stack.pop()


class PersistentStack:
    class Node:
        def __init__(self, data, predecessor: PersistentStack.Node = None):
            self.data = data
            self.predecessor = predecessor

        def __str__(self):
            return str(self.data)

    def __init__(self, size: int = 0, head: PersistentStack.Node = None):
        self.size = size
        self.head = head

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self)) + "]"

    def __iter__(self) -> iter:
        node, queue = self.head, deque()
        while node:
            queue.appendleft(node.data)
            node = node.predecessor
        return iter(queue)

    def __len__(self) -> int:
        return self.size

    def push(self, data) -> PersistentStack:
        """ O(1) """
        if self.size == 0:
            return PersistentStack(1, self.Node(data, None))
        return PersistentStack(self.size + 1, self.Node(data, self.head))

    def pop(self) -> PersistentStack:
        """ O(1) """
        if self.size == 0:
            raise IndexError("Pop from empty stack")
        return PersistentStack(self.size - 1, self.head.predecessor)

    def top(self, k: int = 1, always_return_list: bool = False):
        """ O(k) """
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.head.data] if always_return_list else self.head.data
        else:
            node, output = self.head, list()
            for _ in range(k):
                output.append(node.data)
                node = node.predecessor
            return output

