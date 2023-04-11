from collections import MutableSequence
from typing import Callable, Iterable
from ezcode.Heap.PriorityQueue import PriorityQueue


class PriorityMap(PriorityQueue):
    def __init__(self, init_data: Iterable = None, min_heap: bool = True, key: Callable = None, unpack_pairs: bool = True):
        self.map = dict()  # <item, heap_index>
        super().__init__(init_data=init_data, min_heap=min_heap, key=key, unpack_pairs=unpack_pairs)

    def __contains__(self, item) -> bool:
        return item in self.map

    def __delitem__(self, item):  # O(logN)
        if item not in self.map:
            raise KeyError(f"{item} not found")
        index = self.map[item]
        if index == len(self) - 1:  # the key to delete is at the end of heap
            del self.map[item]
            return self.heap.pop()
        else:
            tail = self.heap[-1]
            self.heap[index] = tail
            self.map[tail[0]] = index
            del self.map[item]
            self.heap.pop()
            self._sift_up(index)

    def __getitem__(self, item):
        """ get priority: O(1) """
        if item not in self.map:
            raise KeyError(f"{item} not found")
        return self.heap[self.map[item]][1]

    def __setitem__(self, item, priority):  # O(logN)
        self.push(item, priority)

    def heapify(self, mutable_sequence: MutableSequence, min_heap: bool = True, key: Callable = None, unpack_pairs: bool = True):
        self.heap.clear()
        self.map.clear()
        self.min_heap = min_heap
        self.key = key
        for index, entry in enumerate(mutable_sequence):
            if isinstance(entry, Iterable) and len(entry) == 2 and unpack_pairs:
                self.heap.append((entry[0], entry[1]))
            else:
                self.heap.append((entry, entry if key is None else key(entry)))
            self.map[entry] = index
        for index in range((len(self.heap) >> 1) - 1, -1, -1):
            self._sift_up(index)

    def push(self, *args, **kwargs):  # O(logN)
        """
        args: (item, priority) / item, priority / item
        kwargs: item=..., priority=...
        """
        item, priority = self._get_item_and_priority(*args, **kwargs)
        if item in self.map:
            self.update(item, priority)
        else:
            self.heap.append((item, priority))
            index = len(self) - 1
            self.map[item] = index
            self._sift_down(index)

    def update_top(self, *args, **kwargs):
        self.update(args=args, kwargs=kwargs)

    def update(self, *args, **kwargs):  # O(logN)
        item, priority = self._get_item_and_priority(*args, **kwargs)
        if item not in self.map:
            raise KeyError(f"{item} not found")
        index = self.map[item]
        old_entry = self.heap[index]
        if old_entry[1] != priority:
            self.heap[index] = (item, priority)
            if (self.min_heap and priority < old_entry[1]) or (not self.min_heap and old_entry[1] < priority):
                self._sift_down(index)  # python sift down is from leaf to root
            else:
                self._sift_up(index)  # python sift up is from root to leaf

    def keys(self):
        yield from self.map.keys()

    def clear(self):
        super().clear()
        self.map.clear()

    def top(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:  # O(1)
            if always_return_list:
                return [self.heap[0]] if with_priority else [self.heap[0][0]]  # [item / (item, priority)]
            return self.heap[0] if with_priority else self.heap[0][0]  # item / (item, priority)
        else:  # O(2N + KlogN)
            pm_copy = PriorityMap(min_heap=self.min_heap, key=self.key)
            pm_copy.heap = self.heap.copy()  # shallow copy: O(N)
            pm_copy.map = self.map.copy()    # shallow copy: O(N)
            return pm_copy.pop(k, with_priority)  # [item / (item, priority)], O(KlogN)

    def pop(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:  # O(logN)
            head = self.heap[0]  # (item, priority)
            self.heap[0] = self.heap[-1]
            self.map[self.heap[0][0]] = 0  # item index = 0
            self.heap.pop()
            del self.map[head[0]]
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

    def _sift_down(self, index: int):
        """ python sift down is from leaf to root, O(logN) """
        tmp_entry = self.heap[index]
        while index > 0:
            parent_index = (index - 1) >> 1
            parent = self.heap[parent_index]
            if (self.min_heap and tmp_entry[1] < parent[1]) or (not self.min_heap and parent[1] < tmp_entry[1]):
                self.heap[index] = parent
                self.map[parent[0]] = index
                index = parent_index
            else:
                break
        self.heap[index] = tmp_entry
        self.map[tmp_entry[0]] = index

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
                if (self.min_heap and right_child[1] < left_child[1]) or (not self.min_heap and left_child[1] < right_child[1]):
                    child_index = right_index
            child = self.heap[child_index]
            if (self.min_heap and child[1] < tmp_entry[1]) or (not self.min_heap and tmp_entry[1] < child[1]):
                self.heap[index] = child
                self.map[child[0]] = index
                index = child_index
                left_index = (index << 1) + 1
            else:
                break
        self.heap[index] = tmp_entry
        self.map[tmp_entry[0]] = index


