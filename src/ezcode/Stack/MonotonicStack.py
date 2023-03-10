from ezcode.Stack.Stack import Stack


class MonotonicStack(Stack):
    def __init__(self, reverse: bool = False):
        """
        reverse = False: Monotonic Increasing
        reverse = True: Monotonic Decreasing
        """
        super().__init__()
        self.reverse = reverse

    def push(self, data):
        if self.reverse:
            while len(self) > 0 and self.list[-1] <= data:
                self.list.pop()
        else:
            while len(self) > 0 and data <= self.list[-1]:
                self.list.pop()
        super().push(data)
