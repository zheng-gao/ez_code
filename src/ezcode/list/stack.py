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


class MinStack:
    def __init__(self):
        self.stack = Stack()
        self.min_stack = Stack()

    def get_min(self):
        return self.min_stack.peek()

    def push(self, data):
        if len(self.min_stack) == 0 or data <= self.min_stack.peek():
            self.min_stack.push(data)
        self.stack.push(data)

    def peek(self):
        return self.stack.peek()

    def pop(self):
        if self.stack.peek() == self.min_stack.peek():
            self.min_stack.pop()
        return self.stack.pop()


class MaxStack:
    def __init__(self):
        self.stack = Stack()
        self.max_stack = Stack()

    def get_max(self):
        return self.max_stack.peek()

    def push(self, data):
        if len(self.max_stack) == 0 or data >= self.max_stack.peek():
            self.max_stack.push(data)
        self.stack.push(data)

    def peek(self):
        return self.stack.peek()

    def pop(self):
        if self.stack.peek() == self.max_stack.peek():
            self.max_stack.pop()
        return self.stack.pop()
