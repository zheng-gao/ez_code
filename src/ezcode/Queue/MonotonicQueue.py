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
            while len(self) > 0 and self.doubly_linked_list.peek_tail() > data:
                self.doubly_linked_list.pop_tail()
        else:
            while len(self) > 0 and self.doubly_linked_list.peek_tail() < data:
                self.doubly_linked_list.pop_tail()
        self.doubly_linked_list.add_to_tail(data)
