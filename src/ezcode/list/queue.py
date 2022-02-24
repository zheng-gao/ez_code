from ezcode.list.const import BACKWARD_LINK
from ezcode.list.linked_list import DoublyLinkedList


class Queue:
    def __init__(self):
        self.doubly_linked_list = DoublyLinkedList()

    def __len__(self):
        return len(self.doubly_linked_list)

    def __str__(self):
        return self.doubly_linked_list.to_string(
            include_end=False,
            backward_link=BACKWARD_LINK,
            bidirection_link=BACKWARD_LINK
        )

    def print(self):
        print(self)

    def push(self, data):
        self.doubly_linked_list.add_to_tail(data)

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peek at an empty queue")
        return self.doubly_linked_list.peek_head()

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty queue")
        return self.doubly_linked_list.pop_head()


class MonotonicQueue(Queue):
    def __init__(self, is_increasing: bool = True):
        """
        Monotonic Increasing Queue: min head
        Monotonic Decreasing Queue: max head
        """
        super().__init__()
        self.is_increasing = is_increasing

    def push(self, data):
        if self.is_increasing:
            while len(self) > 0 and self.doubly_linked_list.peek_tail() > data:
                self.doubly_linked_list.pop_tail()
        else:
            while len(self) > 0 and self.doubly_linked_list.peek_tail() < data:
                self.doubly_linked_list.pop_tail()
        self.doubly_linked_list.add_to_tail(data)

