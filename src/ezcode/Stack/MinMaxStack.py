from ezcode.Stack import Stack


class MinMaxStack:
    def __init__(self):
        self.stack = Stack()
        self.min_so_far = Stack()
        self.max_so_far = Stack()

    def get_min(self):
        return self.min_so_far.top()

    def get_max(self):
        return self.max_so_far.top()

    def push(self, data):
        if len(self.min_so_far) == 0 or data <= self.min_so_far.top():
            self.min_so_far.push(data)
        if len(self.max_so_far) == 0 or self.max_so_far.top() <= data:
            self.max_so_far.push(data)
        self.stack.push(data)

    def top(self, k: int = 1, always_return_list: bool = False):
        return self.stack.top(k, always_return_list)

    def pop(self):
        if self.stack.top() == self.min_so_far.top():
            self.min_so_far.pop()
        if self.stack.top() == self.max_so_far.top():
            self.max_so_far.pop()
        return self.stack.pop()

