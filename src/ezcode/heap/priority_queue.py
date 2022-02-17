import heapq


class PriorityQueue:
    def __init__(self, data: list = None, is_min=True):
        self.is_min = is_min
        if data:
            if self.is_min:
                self.list = data.copy()
            else:
                self.list = [d * -1 for d in data]
            heapq.heapify(self.list)
        else:
            self.list = list()

    def __len__(self):
        return len(self.list)

    def push(self, data):
        if self.is_min:
            heapq.heappush(self.list, data)
        else:
            heapq.heappush(self.list, data * -1)

    def pop(self):
        if len(self) > 0:
            if self.is_min:
                return heapq.heappop(self.list)
            else:
                return heapq.heappop(self.list) * -1
        else:
            raise IndexError("Pop on an empty queue")

    def peek(self):
        if len(self) > 0:
            if self.is_min:
                return self.list[0]
            else:
                return self.list[0] * -1
        else:
            raise IndexError("Peek at an empty queue")