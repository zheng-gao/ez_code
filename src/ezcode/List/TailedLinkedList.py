from typing import Iterable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME
from ezcode.List.LinkedList import LinkedList
from ezcode.List.LinkedListIterator import LinkedListIterator


class TailedLinkedList(LinkedList):
    def __init__(self,
        init_data: Iterable = None, head=None, head_copy=None,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME
    ):
        self.tail = None
        super().__init__(
            init_data=init_data, head=head, head_copy=head_copy,
            data_name=data_name, next_name=next_name
        )

    def _size(self):  # recalculate the size
        """ Time: O(N) """
        self.size = 0
        for node in LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=False, iterate_node=True
        ):
            self.tail = node  # Reset Tail
            self.size += 1
        return self.size

    def __delitem__(self, index: int):
        index = self.regularize_index(index)  # recalculate the index from head
        if index == 0:
            self.head = self.get_next(self.head)
            if self.head is None:
                self.tail = None
        else:
            predecessor = self.get_next(node=self.head, steps=index - 1)
            self.set_next(node=predecessor, next_node=self.get_next(predecessor, steps=2))
            if index == self.size - 1:
                self.tail = predecessor
        self.size -= 1

    def get_node(self, index: int):
        if index == 0 and len(self) > 0:
            return self.tail
        return self.get_next(node=self.head, steps=self.regularize_index(index))

    def remove_all(self, data):
        predecessor, node = None, self.head
        while node is not None:
            next_node = self.get_next(node)
            if data == self.get_data(node):
                if node == self.head:
                    self.head = next_node
                else:
                    self.set_next(node=predecessor, next_node=next_node)
                self.size -= 1
            else:
                predecessor = node
            node = next_node
        if self.head is None:
            self.tail = None
        elif predecessor is not None:
            self.tail = predecessor

    def clear(self):
        super().clear()
        self.tail = None

    def append(self, data):
        super().append(data)
        if self.tail is None:  # len(self) was 0
            self.tail = self.head

    def appendleft(self, data):
        """ Time: O(1) """
        if self.head is None:  # len(self) == 0
            self.head = self.tail = self.new_node(data)
        else:
            self.set_next(node=self.tail, next_node=self.new_node(data))
            self.tail = self.get_next(node=self.tail)
        self.size += 1

    def insert(self, index: int, data):
        super().insert(index, data)
        if self.tail is None:  # len(self) was 0
            self.tail = self.head

    def reverse(self):
        self.tail = self.head
        super().reverse()

    def copy_from_node(self, node):
        if node is None:
            self.clear()
        else:
            if not (self.head is None and self.new_node().match(node)) and not (self.head is not None and self.head.match(node)):
                raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
            node_copy = self.new_node(data=self.get_data(node))
            self.head, self.size = node_copy
            self.tail = node_copy  # diff from parent class, reseting tail
            while self.get_next(node) is not None:
                node = self.get_next(node)
                next_node_copy = self.new_node(data=self.get_data(node))
                self.set_next(node=node_copy, next_node=next_node_copy)
                node_copy = next_node_copy
                self.tail = node_copy  # diff from parent class, reseting tail
                self.size += 1

