from ezcode.list.const import FORWARD_LINK
from ezcode.list.linked_list import DoublyLinkedList


class Queue:
    def __init__(self):
        self.doubly_linked_list = DoublyLinkedList()

    def __len__(self):
        return len(self.doubly_linked_list)

    def __str__(self):
        return self.doubly_linked_list.to_string(
            include_end=False,
            backward_link=FORWARD_LINK,
            bidirection_link=FORWARD_LINK
        )

    def print(self):
        print(self)

    def push(self, data):
        self.doubly_linked_list.add_to_head(data)

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty queue")
        return self.doubly_linked_list.pop_tail()

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peek at an empty queue")
        return self.doubly_linked_list.peek_tail()