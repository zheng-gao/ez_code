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

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peek at an empty stack")
        return self.singly_linked_list.peek_head()

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty stack")
        return self.singly_linked_list.pop_head()


class MinStack:
    def __init__(self):
        self.stack = Stack()
        self.min_stack = Stack()

    def get_min(self):
        return self.min_stack.peek()

    def push(self, data):
        if len(self.min_stack) == 0 or data <= self.min_stack.peek():
            self.min_stack.push(data)
        self.stack.push(data)

    def peek(self):
        return self.stack.peek()

    def pop(self):
        if self.stack.peek() == self.min_stack.peek():
            self.min_stack.pop()
        return self.stack.pop()


class MaxStack:
    def __init__(self):
        self.stack = Stack()
        self.max_stack = Stack()

    def get_max(self):
        return self.max_stack.peek()

    def push(self, data):
        if len(self.max_stack) == 0 or data >= self.max_stack.peek():
            self.max_stack.push(data)
        self.stack.push(data)

    def peek(self):
        return self.stack.peek()

    def pop(self):
        if self.stack.peek() == self.max_stack.peek():
            self.max_stack.pop()
        return self.stack.pop()


class PersistentStack:
    class Node:
        def __init__(self, data, predecessor: PersistentStack.Node = None):
            self.data = data
            self.predecessor = predecessor

        def __str__(self):
            return str(self.data)

    def __init__(self, size: int = 0, top: PersistentStack.Node = None):
        self.size = size
        self.top = top

    def __str__(self) -> str:
        return "[" + ", ".join(map(str, self)) + "]"

    def __iter__(self) -> iter:
        node, queue = self.top, deque()
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
        return PersistentStack(self.size + 1, self.Node(data, self.top))

    def pop(self) -> PersistentStack:
        """ O(1) """
        if self.size == 0:
            raise IndexError("Pop from empty stack")
        return PersistentStack(self.size - 1, self.top.predecessor)

    def top(self, k: int = 1, always_return_list: bool = False):
        """ O(k) """
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.top.data] if always_return_list else self.top.data
        else:
            node, output = self.top, list()
            for _ in range(k):
                output.append(node.data)
                node = node.predecessor
            return output
