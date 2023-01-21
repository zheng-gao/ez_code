from ezcode.List import BACKWARD_LINK
from ezcode.List.DoublyLinkedList import DoublyLinkedList


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

    def top(self, k: int = 1, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.doubly_linked_list.peek_head()] if always_return_list else self.doubly_linked_list.peek_head()
        else:
            node, output = self.doubly_linked_list.head, list()
            for _ in range(k):
                output.append(self.doubly_linked_list.algorithm.get_data(node))
                node = self.doubly_linked_list.algorithm.get_next(node)
            return output

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty queue")
        return self.doubly_linked_list.pop_head()
