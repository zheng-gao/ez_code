from typing import Iterable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, PREV_NAME
from ezcode.List.LinkedListIterator import DoublyLinkedListIterator
from ezcode.List.TailedLinkedList import TailedLinkedList


class DoublyLinkedList(TailedLinkedList):
    def __init__(self,
        init_data: Iterable = None, head=None, head_copy=None,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME, prev_name: str = PREV_NAME
    ):
        self.prev_name = prev_name
        super().__init__(
            init_data=init_data, head=head, head_copy=head_copy,
            data_name=data_name, next_name=next_name
        )

    def new_node(self, data=None, next_node=None, prev_node=None):
        node = super().new_node(data=data, next_node=next_node)
        node.__dict__[self.prev_name] = prev_node
        return node

    def get_prev(self, node, steps: int = 1):
        for _ in range(steps):
            if node is None:
                return None
            node = node.__dict__[self.prev_name]
        return node

    def has_prev(self, node, steps: int = 1) -> bool:
        if not node:
            return False
        for _ in range(steps):
            node = node.__dict__[self.prev_name]
            if not node:
                return False
        return True

    def set_prev(self, node, prev_node=None):
        node.__dict__[self.prev_name] = prev_node

    def get_node(self, index: int):
        r = self.regularize_index(index)
        return self.get_prev(node=self.tail, steps=index) if index < r else self.get_next(node=self.head, steps=r)

    def __iter__(self):
        """ from index 0 (tail) to -1 (head) """
        return DoublyLinkedListIterator(
            head=self.head, tail=self.tail,
            data_name=self.data_name, next_name=self.next_name, prev_name=self.prev_name,
            reverse=True, iterate_node=False
        )

    def __reversed__(self):
        """ from index -1 (head) to 0 (tail) """
        return DoublyLinkedListIterator(
            head=self.head, tail=self.tail,
            data_name=self.data_name, next_name=self.next_name, prev_name=self.prev_name,
            reverse=False, iterate_node=False
        )

    def __delitem__(self, index: int):
        index = self.regularize_index(index)
        if index == 0:
            self.head = self.get_next(self.head)
            if self.head is None:
                self.tail = None
            else:
                self.set_prev(node=self.head, prev_node=None)
        elif index == self.size - 1:
            self.tail = self.get_prev(self.tail)
            if self.tail is None:
                self.head = None
            else:
                self.set_next(node=self.tail, next_node=None)
        else:  # at least 3 nodes exist
            node = self.get_node(index)
            prev_node, next_node = self.get_prev(node), self.get_next(node)
            if prev_node is not None:
                self.set_next(node=prev_node, next_node=next_node)
            if next_node is not None:
                self.set_prev(node=next_node, next_node=prev_node)
        self.size -= 1

    def remove_all(self, data):
        prev_node, node = None, self.head
        while node is not None:
            next_node = self.get_next(node)
            if data == self.get_data(node):
                if node == self.head:
                    self.head = next_node
                else:
                    self.set_next(node=prev_node, next_node=next_node)
                if next_node is not None:
                    self.set_prev(node=next_node, prev_node=prev_node)
                self.size -= 1
            else:
                prev_node = node
            node = next_node
        if self.head is None:
            self.tail = None
        elif prev_node is not None:
            self.tail = prev_node

    def popleft(self):
        if len(self) == 0:
            raise KeyError("Pop from empty list")
        data = self[0]
        del self[0]
        return data

    def append(self, data):
        if self.head is None:  # len(self) == 0
            self.head = self.tail = self.new_node(data)
        else:
            self.set_prev(node=self.head, next_node=self.new_node(data=data, next_node=self.head))
            self.head = self.get_prev(node=self.head)
        self.size += 1

    def appendleft(self, data):
        if self.head is None:  # len(self) == 0
            self.head = self.tail = self.new_node(data)
        else:
            self.set_next(node=self.tail, next_node=self.new_node(data=data, prev_node=self.tail))
            self.tail = self.get_next(node=self.tail)
        self.size += 1

    def insert(self, index: int, data):
        index = self.regularize_index(index, auto_fit=True)
        if index == 0:
            self.append(data)
        elif index == self.size - 1:
            self.appendleft(data)
        else:
            node = self.get_next(node=self.head, steps=index)
            next_node = self.get_next(node)
            inserted_node = self.new_node(data=data, next_node=next_node, prev_node=node)
            self.set_prev(node=next_node, prev_node=inserted_node)
            self.set_next(node=node, next_node=inserted_node)
            self.size += 1

    def copy_from_node(self, node):
        if node is None:
            self.clear()
        else:
            if not (self.head is None and self.new_node().match(node)) and not (self.head is not None and self.head.match(node)):
                raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
            node_copy = self.new_node(data=self.get_data(node))
            self.head, self.size = node_copy
            self.tail = node_copy
            while self.get_next(node) is not None:
                node = self.get_next(node)
                next_node_copy = self.new_node(data=self.get_data(node))
                if next_node_copy is not None:
                    self.set_prev(node=next_node_copy, prev_node=node_copy)  # diff from parent class, setting prev_node
                self.set_next(node=node_copy, next_node=next_node_copy)
                node_copy = next_node_copy
                self.tail = node_copy
                self.size += 1

    def copy_from(self, other):
        if isinstance(other, self.__class__):
            self.data_name = other.data_name
            self.next_name = other.next_name
            self.prev_name = other.prev_name  # diff from parent class
            self.copy_from_node(other.head)

    def reverse(self):
        node = self.tail
        while node is not None:
            prev_node = self.get_prev(node)
            next_node = self.get_next(node)
            self.set_prev(node=node, prev_node=next_node)
            self.set_next(node=node, next_node=prev_node)
            node = next_node
        self.head, self.tail = self.tail, self.head






