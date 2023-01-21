from typing import Callable
from typing import Iterable


class PriorityQueueOnPartialArray:
    def __init__(self, array: list, min_heap: bool = True, key: Callable = lambda x: x, start: int = 0, end: int = None, init_queue: Iterable = None):
        self.min_heap = min_heap
        self.key = key
        self.heap = array
        self.start = start
        self.end = start - 1
        self.max_end = end if end else len(array) - 1
        if init_queue is not None:
            for item in init_queue:
                self.push(item)

    def __len__(self):
        return self.end - self.start + 1

    def __str__(self):
        return str(self.heap[self.start:self.end + 1])

    def clear(self):
        self.end = self.start - 1

    def is_full(self):
        return self.end == self.max_end

    def is_empty(self):
        return self.end == self.start - 1

    def items(self, with_priority=False):
        if with_priority:
            return [(item, self.key(item)) for item in self.heap[self.start:self.end + 1]]
        return self.heap[self.start:self.end + 1]

    def push(self, item):  # O(logN)
        if self.is_full():
            raise IndexError("The queue is full.")
        self.end += 1
        self.heap[self.end] = item
        self._sift_down(self.end)

    def top(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:  # O(1)
            if always_return_list:
                return [(self.heap[self.start], self.key(self.heap[self.start]))] if with_priority else [self.heap[self.start]]
            return (self.heap[self.start], self.key(self.heap[self.start])) if with_priority else self.heap[self.start]
        else:  # O(N + KlogN)
            pq_copy = PriorityQueueOnPartialArray(
                array=self.heap[self.start:self.end + 1],
                min_heap=self.min_heap, key=self.key, start=0
            )  # shallow copy: O(N)
            return pq_copy.pop(k)  # [item], O(KlogN)

    def pop(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, queue size: {len(self)}, k: {k}")
        if k == 1:  # O(logN)
            head = self.heap[self.start]
            self.heap[self.start] = self.heap[self.end]
            self.end -= 1
            if len(self) > 1:
                self._sift_up(self.start)
            if always_return_list:
                return [(head, self.key(head))] if with_priority else [head]
            return (head, self.key(head)) if with_priority else head
        else:  # O(KlogN)
            pop_list = list()
            while k > 0:  # O(KlogN)
                pop_list.append(self.pop(1, with_priority, False))  # O(logN)
                k -= 1
            return pop_list  # [item / (item, priority)]

    def update_top(self, item):
        """ O(logN) """
        if self.is_empty():
            raise IndexError("Empty queue has no top")
        self.heap[self.start] = item
        self._sift_up(0)  # python sift up is from root to leaf

    def _sift_down(self, index: int):
        """ python sift down is from leaf to root, O(logN) """
        item = self.heap[index]
        item_priority = self.key(item)
        while index > self.start:
            parent_index = ((index - self.start - 1) >> 1) + self.start
            parent = self.heap[parent_index]
            parent_priority = self.key(parent)
            if (self.min_heap and item_priority < parent_priority) or (not self.min_heap and parent_priority < item_priority):
                self.heap[index] = parent
                index = parent_index
            else:
                break
        self.heap[index] = item

    def _sift_up(self, index: int):
        """ python sift up is from root to leaf, O(logN) """
        item = self.heap[index]
        item_priority = self.key(item)
        left_index = ((index - self.start) << 1) + 1 + self.start
        while left_index <= self.end:
            right_index = left_index + 1
            child_index = left_index
            if right_index <= self.end:
                left_priority, right_priority = self.key(self.heap[left_index]), self.key(self.heap[right_index])
                if (self.min_heap and right_priority < left_priority) or (not self.min_heap and left_priority < right_priority):
                    child_index = right_index
            child = self.heap[child_index]
            child_priority = self.key(child)
            if (self.min_heap and child_priority < item_priority) or (not self.min_heap and item_priority < child_priority):
                self.heap[index] = child
                index = child_index
                left_index = ((index - self.start) << 1) + 1 + self.start
            else:
                break
        self.heap[index] = item



