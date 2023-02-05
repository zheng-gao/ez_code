from collections.abc import MutableSequence
from typing import Iterable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME
from ezcode.List.LinkedListIterator import LinkedListIterator


class LinkedList(MutableSequence):
    class LinkedListNode:
        def __init__(self):
            pass

        def match(self, other) -> bool:
            if any(key not in self.__dict__.keys() for key in other.__dict__.keys()):
                return False
            if any(key not in other.__dict__.keys() for key in self.__dict__.keys()):
                return False
            return True

    def __init__(self,
        init_data: Iterable = None, head=None, head_copy=None,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME
    ):
        self.head, self.size = head, 0
        self.data_name = data_name
        self.next_name = next_name
        if head is not None:  # Any change on this list will affect the original list on the head
            self._size()
        elif head_copy is not None:
            self.copy_from(head_copy)
        if init_data is not None:
            for data in init_data:
                self.append(data)

    def new_node(self, data=None, next_node=None):
        node = self.LinkedListNode()
        node.__dict__ = {self.data_name: data, self.next_name: next_node}
        return node

    def get_data(self, node):
        return node.__dict__[self.data_name]

    def set_data(self, node, data):
        node.__dict__[self.data_name] = data

    def get_next(self, node, steps: int = 1):
        for _ in range(steps):
            if node is None:
                return None
            node = node.__dict__[self.next_name]
        return node

    def set_next(self, node, next_node=None):
        node.__dict__[self.next_name] = next_node

    def __iter__(self):
        """ from index 0 (last element) to head """
        return LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=True, iterate_node=False
        )

    def __reversed__(self):
        """ from index -1 (first/head element) to end """
        return LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=False, iterate_node=False
        )

    def __contains__(self, data):
        return any(d == data for d in reversed(self))

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int):
        return self.get_data(self.get_next(node=self.head, steps=self._revert_index(index)))

    def __setitem__(self, index: int, data):
        self.set_data(node=self.get_next(node=self.head, steps=self._revert_index(index)), data=data)

    def __delitem__(self, index: int):
        index = self._revert_index(index)
        if index == 0:
            self.head = self.get_next(self.head)
        else:
            predecessor = self.get_next(node=self.head, steps=index - 1)
            self.set_next(node=predecessor, next_node=self.get_next(self.get_next(predecessor)))
        self.size -= 1

    def __iadd__(self, other: Iterable):
        self.extend(other)

    def _size(self):  # recalculate the size
        self.size = 0
        for _ in reversed(self):
            self.size += 1

    def _revert_index(self, index):
        if index > self.size - 1 or index < -self.size:
            raise IndexError(f"list index {index} out of range")
        return self.size - 1 - index if index > 0 else -1 - self.size

    def clear(self):
        self.head, self.size = None, 0

    def count(self, data):
        occurrences = 0
        for d in reversed(self):
            if data == d:
                occurrences += 1
        return occurrences

    def copy(self):
        list_copy = self.__class__()
        list_copy.copy_from(self)
        return list_copy

    def copy_from_node(self, node):
        if node is None:
            self.clear()
        else:
            if not (self.head is None and self.new_node().match(node)) and not (self.head is not None and self.head.match(node)):
                raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
            node_copy = self.new_node(data=self.get_data(node))
            self.head, self.size = node_copy, 1
            while self.get_next(node) is not None:
                node = self.get_next(node)
                self.set_next(node=node_copy, next_node=self.new_node(data=self.get_data(node)))
                node_copy = self.get_next(node_copy)
                self.size += 1

    def copy_from(self, other):
        if isinstance(other, self.__class__):
            self.data_name = other.data_name
            self.next_name = other.next_name
            self.copy_from_node(other.head)

    def extend(self, other: Iterable):
        for data in other:
            self.append(data)

    def append(self, data):
        self.head = self.new_node(data=data, next_node=self.head)
        self.size += 1

    def insert(self, index: int, data):
        index = self._revert_index(index)
        if index == 0:
            self.head = self.new_node(data=data, next_node=self.head)
        else:
            predecessor = self.get_next(node=self.head, steps=index - 1)
            self.set_next(node=predecessor, next_node=self.new_node(data=data, next_node=self.get_next(predecessor)))
        self.size += 1

    def remove(self, data):
        predecessor, node = None, self.head
        while node is not None:
            if data == self.get_data(node):
                if node == self.head:
                    self.head = self.get_next(self.head)
                else:
                    self.set_next(node=predecessor, next_node=self.get_next(self.get_next(predecessor)))
                self.size -= 1
                return
            predecessor, node = node, self.get_next(node)
        raise ValueError(f"{data} not found")

    def reverse(self):
        predecessor, node = None, self.head
        while node is not None:
            successor = self.get_next(node)
            self.set_next(node=node, next_node=predecessor)
            predecessor, node = node, successor
        self.head = predecessor

    def pop(self):
        if self.size == 0:
            raise KeyError("Pop from empty list")
        data = self.get_data(self.head)
        self.head = self.get_next(self.head)
        self.size -= 1
        return data



