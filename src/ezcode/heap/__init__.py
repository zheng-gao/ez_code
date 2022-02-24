import heapq


# class PriorityQueue:
#     def __init__(self, data: list = None, min_heap: bool = True):
#         self.min_heap = min_heap
#         self.heap = data.copy() if data else list()  # (priority, key)
#         if self.min_heap:
#             heapq.heapify(self.heap)
#         else:
#             heapq._heapify_max(self.heap)
# 
#     def __len__(self):
#         return len(self.heap)
# 
#     def __str__(self):
#         return str(self.heap)
# 
#     def peek(self):
#         """ O(1) """
#         if len(self) <= 0:
#             raise IndexError("Peek at an empty queue")
#         return self.heap[0]
# 
#     def push(self, data):
#         """ O(logN) """
#         if self.min_heap:
#             heapq.heappush(self.heap, data)
#         else:
#             self.heap.append(data)
#             heapq._siftdown_max(self.heap, 0, len(self.heap) - 1)  # python siftdown is from leaf to root
# 
#     def pop(self):
#         """ O(logN) """
#         if len(self) <= 0:
#             raise IndexError("Pop on an empty queue")
#         return heapq.heappop(self.heap) if self.min_heap else heapq._heappop_max(self.heap)


class PriorityQueue:
    def __init__(self, init_queue: list = None, min_heap: bool = True):
        self.min_heap = min_heap
        self.heap = list()  # (priority, key)
        if init_queue:
            for item in init_queue:
                self.push(item)

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)

    def peek(self):
        """ O(1) """
        if len(self) <= 0:
            raise IndexError("Peek at an empty queue")
        return self.heap[0][0] if len(self.heap[0]) == 1 else self.heap[0]  # priority / priority, key

    def push(self, *priority_n_key):
        """ O(logN) """
        if len(priority_n_key) == 0:
            raise KeyError("Nothing to push")
        elif len(priority_n_key) == 1:
            self.heap.append(priority_n_key[0] if type(priority_n_key[0]) is tuple else (priority_n_key[0],))
        else:
            self.heap.append((priority_n_key[0], priority_n_key[1]))
        self._sift_down(len(self.heap) - 1)

    def pop(self):
        """ O(logN) """
        if len(self) <= 0:
            raise IndexError("Pop from an empty queue")
        else:
            top_item = self.heap[0]
            self.heap[0] = self.heap[-1]
            self.heap.pop()
            if len(self) > 0:
                self._sift_up(0)
            return top_item[0] if len(top_item) == 1 else top_item  # priority / priority, key

    def _sift_down(self, index: int):
        """ python sift down is from leaf to root, O(logN) """
        new_item = self.heap[index]
        while index > 0:
            parent_index = (index - 1) >> 1
            parent = self.heap[parent_index]
            if (self.min_heap and new_item[0] < parent[0]) or (not self.min_heap and new_item[0] > parent[0]):
                self.heap[index] = parent
                index = parent_index
            else:
                break
        self.heap[index] = new_item

    def _sift_up(self, index: int):
        """ python sift up is from root to leaf, O(logN) """
        end_index = len(self.heap) - 1
        new_item = self.heap[index]
        left_index = (index << 1) + 1
        while left_index <= end_index:
            right_index = left_index + 1
            child_index = left_index
            if right_index <= end_index:
                left_child, right_child = self.heap[left_index], self.heap[right_index]
                if (self.min_heap and right_child[0] < left_child[0]) or (not self.min_heap and right_child[0] > left_child[0]):
                    child_index = right_index
            child = self.heap[child_index]
            if (self.min_heap and child[0] < new_item[0]) or (not self.min_heap and child[0] > new_item[0]):
                self.heap[index] = child
                index = child_index
                left_index = (index << 1) + 1
            else:
                break
        self.heap[index] = new_item


class PriorityMap(PriorityQueue):
    def __init__(self, init_map: dict = None, min_heap: bool = True):
        super().__init__(min_heap=min_heap)
        self.map = dict() # <key, heap_index>
        if init_map:
            for key, priority in init_map.items():
                self.push(priority, key)

    def __contains__(self, key):
        return key in self.map

    def get_priority(self, key):
        """ O(1) """
        if key not in self:
            raise KeyError(f"{key} not found")
        return self.heap[self.map[key]][0]

    def peek(self):
        """ O(1) """
        if len(self) <= 0:
            raise IndexError("Peek at an empty queue")
        return self.heap[0]

    def push(self, *priority_n_key):
        """ O(logN) """
        priority, key = priority_n_key[0] if type(priority_n_key[0]) is tuple else (priority_n_key[0], priority_n_key[1])
        if key in self:
            self.update(priority, key)
        else:
            self.heap.append((priority, key))
            index = len(self.heap) - 1
            self.map[key] = index
            self._sift_down(index)

    def pop(self):
        """ O(logN) """
        if len(self) <= 0:
            raise IndexError("Pop from an empty queue")
        else:
            top_item = self.heap[0]
            tail_item = self.heap[-1]
            self.heap[0] = tail_item
            self.map[tail_item[1]] = 0
            self.heap.pop()
            del self.map[top_item[1]]
            if len(self) > 0:
                self._sift_up(0)
            return top_item  # priority, key

    def delete(self, key):
        """ O(logN) """
        if key not in self:
            raise KeyError(f"{key} not found")
        index = self.map[key]
        tail_item = self.heap[-1]
        self.map[tail_item[1]] = index
        self.heap[index] = tail_item
        del self.map[key]
        self.heap.pop()
        self._sift_up(index)

    def update(self, *priority_n_key):
        """ O(logN) """
        priority, key = priority_n_key[0] if type(priority_n_key[0]) is tuple else (priority_n_key[0], priority_n_key[1])
        if key not in self:
            raise KeyError(f"{key} not found")
        index = self.map[key]
        old_item = self.heap[index]
        if old_item[0] != priority:
            self.heap[index] = (priority, key)
            if (self.min_heap and priority < old_item[0]) or (not self.min_heap and priority > old_item[0]):
                self._sift_down(index)  # python sift down is from leaf to root
            else:
                self._sift_up(index)  # python sift up is from root to leaf

    def _sift_down(self, index: int):
        """ python sift down is from leaf to root, O(logN) """
        new_item = self.heap[index]
        while index > 0:
            parent_index = (index - 1) >> 1
            parent = self.heap[parent_index]
            if (self.min_heap and new_item[0] < parent[0]) or (not self.min_heap and new_item[0] > parent[0]):
                self.heap[index] = parent
                self.map[parent[1]] = index
                index = parent_index
            else:
                break
        self.heap[index] = new_item
        self.map[new_item[1]] = index

    def _sift_up(self, index: int):
        """ python sift up is from root to leaf, O(logN) """
        end_index = len(self.heap) - 1
        new_item = self.heap[index]
        left_index = (index << 1) + 1
        while left_index <= end_index:
            right_index = left_index + 1
            child_index = left_index
            if right_index <= end_index:
                left_child, right_child = self.heap[left_index], self.heap[right_index]
                if (self.min_heap and right_child[0] < left_child[0]) or (not self.min_heap and right_child[0] > left_child[0]):
                    child_index = right_index
            child = self.heap[child_index]
            if (self.min_heap and child[0] < new_item[0]) or (not self.min_heap and child[0] > new_item[0]):
                self.heap[index] = child
                self.map[child[1]] = index
                index = child_index
                left_index = (index << 1) + 1
            else:
                break
        self.heap[index] = new_item
        self.map[new_item[1]] = index




