import heapq


class PriorityQueue:
    def __init__(self, data: list = None, min_heap: bool = True):
        self.min_heap = min_heap
        self.heap = data.copy() if data else list()
        if self.min_heap:
            heapq.heapify(self.heap)
        else:
            heapq._heapify_max(self.heap)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)

    def push(self, data):
        if self.min_heap:
            heapq.heappush(self.heap, data)
        else:
            self.heap.append(data)
            heapq._siftdown_max(self.heap, 0, len(self.heap) - 1)

    def pop(self):
        if len(self) > 0:
            if self.min_heap:
                return heapq.heappop(self.heap)
            else:
                return heapq._heappop_max(self.heap)
        else:
            raise IndexError("Pop on an empty queue")

    def peek(self):
        if len(self) > 0:
            return self.heap[0]
        else:
            raise IndexError("Peek at an empty queue")

