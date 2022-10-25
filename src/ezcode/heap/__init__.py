from typing import Callable


class PriorityQueue:
    def __init__(self, init_queue: list = None, min_heap: bool = True, key: Callable = lambda x: x):
        self.min_heap = min_heap
        self.key = key
        self.heap = list()  # [(item, priority)]
        if init_queue is not None:
            for entry in init_queue:
                self.push(entry)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)

    def items(self, with_priority=False):
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
            if type(args[0]) is tuple:
                item, priority = args[0]
            else:
                item, priority = args[0], self.key(args[0])
        elif len_args == 2:
            item, priority = args
        else:
            if "item" not in kwargs:
                raise ValueError(f"Invalid kwargs, must contains \"item\": {kwargs}")
            item = kwargs["item"]
            priority = kwargs["priority"] if "priority" in kwargs else self.key(item)
        return item, priority

    def push(self, *args, **kwargs):  # O(logN)
        """
        args: (item, priority) / item, priority / item
        kwargs: item=..., priority=...
        """
        self.heap.append(self._get_item_and_priority(*args, **kwargs))
        self._sift_down(len(self.heap) - 1)

    def top(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self.heap) < k:
            raise ValueError(f"Not enough items, size: {len(self.heap)}, k: {k}")
        if k == 1:  # O(1)
            if always_return_list:
                return [self.heap[0]] if with_priority else [self.heap[0][0]]  # [item / (item, priority)]
            return self.heap[0] if with_priority else self.heap[0][0]  # item / (item, priority)
        else:  # O(N + KlogN)
            pq_copy = PriorityQueue(min_heap=self.min_heap, key=self.key)
            pq_copy.heap = self.heap.copy()  # shallow copy: O(N)
            return pq_copy.pop(k, with_priority)  # [item / (item, priority)], O(KlogN)

    def pop(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self.heap) < k:
            raise ValueError(f"Not enough items, queue size: {len(self.heap)}, k: {k}")
        if k == 1:  # O(logN)
            head = self.heap[0]
            self.heap[0] = self.heap[-1]
            self.heap.pop()
            if len(self.heap) > 1:
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
        if len(self.heap) == 0:
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
            if (self.min_heap and tmp_entry[1] < parent[1]) or (not self.min_heap and parent[1] < tmp_entry[1]):
                self.heap[index] = parent
                index = parent_index
            else:
                break
        self.heap[index] = tmp_entry

    def _sift_up(self, index: int):
        """ python sift up is from root to leaf, O(logN) """
        tmp_entry = self.heap[index]
        end_index = len(self.heap) - 1
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
                index = child_index
                left_index = (index << 1) + 1
            else:
                break
        self.heap[index] = tmp_entry


class PriorityMap(PriorityQueue):
    def __init__(self, init_map: dict = None, min_heap: bool = True, key: Callable = lambda x: x):
        super().__init__(min_heap=min_heap, key=key)
        self.map = dict()  # <item, heap_index>
        if init_map is not None:
            for item, priority in init_map.items():
                self.push(item, priority)

    def __contains__(self, item):
        return item in self.map

    def __delitem__(self, item):  # O(logN)
        if item not in self.map:
            raise KeyError(f"{item} not found")
        index = self.map[item]
        if index == len(self.heap) - 1:  # the key to delete is at the end of heap
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
            index = len(self.heap) - 1
            self.map[item] = index
            self._sift_down(index)

    def update(self, *args, **kwargs):   # O(logN)
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
        return self.map.keys()

    def clear(self):
        super().clear()
        self.map.clear()

    def top(self, k: int = 1, with_priority: bool = False, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self.heap) < k:
            raise ValueError(f"Not enough items, size: {len(self.heap)}, k: {k}")
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
        if len(self.heap) < k:
            raise ValueError(f"Not enough items, size: {len(self.heap)}, k: {k}")
        if k == 1:  # O(logN)
            head = self.heap[0]  # (item, priority)
            self.heap[0] = self.heap[-1]
            self.map[self.heap[0][0]] = 0  # item index = 0
            self.heap.pop()
            del self.map[head[0]]
            if len(self.heap) > 1:
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
        end_index = len(self.heap) - 1
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


class PriorityQueueOnPartialArray:
    def __init__(self, array: list, min_heap: bool = True, key: Callable = lambda x: x, start: int = 0, end: int = None, init_queue: list = None):
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

