from typing import Callable, Iterable
from collections.abc import Mapping


class PriorityQueue:
    def __init__(self, init_data: Iterable = None, reverse: bool = False, key: Callable = None, unpack_pairs: bool = True):
        """
            reverse: False - Min Heap (default), True - Max Heap
            unpack_pairs: init_data = [(item, priority), ...]
        """
        self.reverse = reverse
        self.key = key
        self.heap = list()  # [(item, priority)]
        if init_data is not None:
            if isinstance(init_data, Mapping):
                for item, priority in init_data.items():
                    self.heap.append((item, priority))
            else:
                for entry in init_data:
                    if isinstance(entry, Iterable) and len(entry) == 2 and unpack_pairs:
                        self.heap.append((entry[0], entry[1]))
                    else:
                        self.heap.append((entry, entry if key is None else key(entry)))
            self._heapify()

    def __len__(self) -> int:
        return len(self.heap)

    def __str__(self) -> str:
        return str(self.heap)

    def is_empty(self) -> bool:
        return len(self) == 0

    def items(self, with_priority=False) -> list:
        if with_priority:
            return self.heap
        return [item for item, _ in self.heap]

    def clear(self):
        self.heap.clear()

    def _get_item_and_priority(self, *args, **kwargs):
        len_args, len_kwargs = len(args), len(kwargs)
        if len_args == 0 and len_kwargs == 0:
            raise KeyError("Nothing to push")
        if len_args != 0 and len_kwargs != 0:
            raise KeyError("Can only push one item at a time")
        if len_args > 2:
            raise ValueError("Cannot take more than 2 args")
        if len_args == 1:
            item = args[0]
            priority = item if self.key is None else self.key(item)
        elif len_args == 2:
            item, priority = args[0], args[1]
        else:
            if "item" not in kwargs:
                raise ValueError(f"Invalid kwargs, must contains \"item\": {kwargs}")
            item = kwargs["item"]
            if "priority" in kwargs:
                priority = kwargs["priority"]
            else:
                priority = item if self.key is None else self.key(item)
        return item, priority

    def _heapify(self):  # O(N)
        for index in range((len(self.heap) >> 1) - 1, -1, -1):
            self._sift_up(index)

    def push(self, *args, **kwargs):  # O(logN)
        """
        args: (item, priority) / [item, priority] / item, priority / item
        kwargs: item=..., priority=...
        """
        self.heap.append(self._get_item_and_priority(*args, **kwargs))
        self._sift_down(len(self) - 1)

    def top(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:  # O(1)
            if always_return_list:
                return [self.heap[0]] if with_priority else [self.heap[0][0]]  # [item / (item, priority)]
            return self.heap[0] if with_priority else self.heap[0][0]  # item / (item, priority)
        else:  # O(N + KlogN)
            pq_copy = PriorityQueue(reverse=self.reverse, key=self.key)
            pq_copy.heap = self.heap.copy()  # shallow copy: O(N)
            return pq_copy.pop(k, with_priority)  # [item / (item, priority)], O(KlogN)

    def pop(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, queue size: {len(self)}, k: {k}")
        if k == 1:  # O(logN)
            head = self.heap[0]
            self.heap[0] = self.heap[-1]
            self.heap.pop()
            if len(self) > 1:
                self._sift_up(0)
            if always_return_list:
                return [head] if with_priority else [head[0]]  # [item / (item, priority)]
            return head if with_priority else head[0]  # item / (item, priority)
        else:  # O(KlogN)
            pop_list = list()
            while k > 0:  # O(KlogN)
                pop_list.append(self.pop(1, with_priority, False))  # O(logN)
                k -= 1
            return pop_list  # [item / (item, priority)]

    def update_top(self, *args, **kwargs):
        """ O(logN) """
        if self.is_empty():
            raise IndexError("Empty queue has no top")
        item, priority = self._get_item_and_priority(*args, **kwargs)
        if self.heap[0][1] != priority:
            self.heap[0] = (item, priority)
            self._sift_up(0)  # python sift up is from root to leaf

    def _sift_down(self, index: int):
        """ python sift down is from leaf to root, O(logN) """
        tmp_entry = self.heap[index]
        while index > 0:
            parent_index = (index - 1) >> 1
            parent = self.heap[parent_index]
            if (not self.reverse and tmp_entry[1] < parent[1]) or (self.reverse and parent[1] < tmp_entry[1]):
                self.heap[index] = parent
                index = parent_index
            else:
                break
        self.heap[index] = tmp_entry

    def _sift_up(self, index: int):
        """ python sift up is from root to leaf, O(logN) """
        tmp_entry = self.heap[index]
        end_index = len(self) - 1
        left_index = (index << 1) + 1
        while left_index <= end_index:
            right_index = left_index + 1
            child_index = left_index
            if right_index <= end_index:
                left_child, right_child = self.heap[left_index], self.heap[right_index]
                if (not self.reverse and right_child[1] < left_child[1]) or (self.reverse and left_child[1] < right_child[1]):
                    child_index = right_index
            child = self.heap[child_index]
            if (not self.reverse and child[1] < tmp_entry[1]) or (self.reverse and tmp_entry[1] < child[1]):
                self.heap[index] = child
                index = child_index
                left_index = (index << 1) + 1
            else:
                break
        self.heap[index] = tmp_entry

