from typing import Iterable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME
from ezcode.List.LinkedList import LinkedList
from ezcdoe.List.LinkedListIterator import LinkedListIterator


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
        self.size = 0
        for node in LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=False, iterate_node=True
        ):
            self.tail = node
            self.size += 1

    def _insert_reset_tail(self):
        if self.tail is None:  # len(self) was 0
            self.tail = self.head

    def _remove_reset_tail(self):
        if self.head is None:  # len(self) == 0
            self.tail = None

    def __delitem__(self, index: int):
        super.__delitem__(index)
        self._remove_reset_tail()

    def remove(self, data):
        super.remove(data)
        self._remove_reset_tail()

    def pop(self):
        data = super().pop()
        self._remove_reset_tail()
        return data

    def clear(self):
        super().clear()
        self._remove_reset_tail()

    def append(self, data):
        super().append(data)
        self._insert_reset_tail()

    def insert(self, index: int, data):
        super().insert(index, data)
        self._insert_reset_tail()

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
            self.head, self.tail, self.size = node_copy, 1  # diff from parent class, reseting tail
            while self.get_next(node) is not None:
                node = self.get_next(node)
                self.set_next(node=node_copy, next_node=self.new_node(data=self.get_data(node)))
                node_copy = self.get_next(node_copy)
                self.tail = node_copy  # diff from parent class, reseting tail
                self.size += 1

