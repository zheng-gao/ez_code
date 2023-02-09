from ezcode.Queue import Queue


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
            while len(self) > 0 and data < self.list[-1]:
                self.list.pop()
        else:
            while len(self) > 0 and self.list[-1] < data:
                self.list.pop()
        self.list.appendleft(data)

    def pop(self):
        return self.list.pop()
