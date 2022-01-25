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

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty stack")
        return self.singly_linked_list.pop_head()

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peek at an empty stack")
        return self.singly_linked_list.peek_head()