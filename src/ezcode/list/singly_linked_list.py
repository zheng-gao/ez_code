from __future__ import annotations

from ezcode.list.const import *
from ezcode.list.algorithm import SinglyLinkedListAlgorithm


class SinglyLinkedList(object):

    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.head = head
        self.data_name = data_name
        self.next_name = next_name
        self.algorithm = SinglyLinkedListAlgorithm(data_name, next_name)

    def new_node(self, data):
        node = self.FakeNode()
        node.__dict__ = {self.data_name: data, self.next_name: None}
        return node

    def print(self, reverse=False):
        if reverse:
            self.algorithm.reverse_print(self.head, self.head)
        else:
            node = self.head
            while node and node.__dict__[self.next_name]:
                print(f"{node.__dict__[self.data_name]} -> ", end="")
                node = node.__dict__[self.next_name]
            if node:
                print(f"{node.__dict__[self.data_name]} -> ", end="")
            print("None")

    def to_array(self):
        array = list()
        node = self.head
        while node:
            array.append(node.__dict__[self.data_name])
            node = node.next
        return array

    def copy(self):
        if not self.head:
            return None
        other_head = self.new_node(self.head.__dict__[self.data_name])
        other_node = other_head
        self_node = self.head.__dict__[self.next_name]
        while self_node:
            other_node.__dict__[self.next_name] = self.new_node(self_node.__dict__[self.data_name])
            self_node = self_node.__dict__[self.next_name]
            other_node = other_node.__dict__[self.next_name]
        return SinglyLinkedList(other_head, self.data_name, self.next_name)

    def is_copied(self, other_list: SinglyLinkedList) -> bool:
        other_head = other_list.head
        if self.head:
            self_node = self.head
            other_node = other_head
            while self_node:
                if self_node.__dict__[self.data_name] != other_node.__dict__[self.data_name]:
                    return False
                self_node = self_node.__dict__[self.next_name]
                other_node = other_node.__dict__[self.next_name]
            return True
        else:
            return other_head == None

    def reverse(self):
        if self.head:
            # self.head = self.algorithm.reverse(self.head, self.head.__dict__[self.next_name])
            previous_node, current_node, next_node = None, self.head, self.head.__dict__[self.next_name]
            while next_node:
                current_node.__dict__[self.next_name] = previous_node
                previous_node = current_node
                current_node = next_node
                next_node = next_node.__dict__[self.next_name]
            self.head = current_node



            

