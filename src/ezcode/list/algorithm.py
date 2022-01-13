from ezcode.list.const import *


class SinglyLinkedListAlgorithm:
    """ Recursion Helpers """

    def __init__(self, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.data_name = data_name
        self.next_name = next_name

    def reverse_print(self, node, head):
        if not node:
            print(f"{node} <- ", end="")
        self.reverse_print(node.__dict__[self.next_name])
        if node == head:
            print(f"{node.__dict__[self.data_name]}")
        else:
            print(f"{node.__dict__[self.data_name]} <- ", end="")

    def reverse(self, previous, current):
        """ head = reverse(head, head.next) """
        if current:
            head = self.reverse(current, current.__dict__[self.next_name])
            current.__dict__[self.next_name] = previous
            previous.__dict__[self.next_name] = None
            return head
        else:
            return previous
