"""
from ezcode.Queue.Queue import Queue


class MonotonicQueue(Queue):
    def __init__(self, reverse: bool = False):
        # reverse = False: Monotonic Increasing
        # reverse = True: Monotonic Decreasing

        super().__init__()
        self.reverse = reverse

    def push(self, data):
        if self.reverse:
            while len(self) > 0 and data < self.list[-1]:
                self.list.pop()
        else:
            while len(self) > 0 and data < self.list[0]:
                self.list.pop()
        self.list.appendleft(data)

    def pop(self):
        return self.list.pop()
"""
