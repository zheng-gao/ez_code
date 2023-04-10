from typing import Callable
from ezcode.Heap.PriorityQueue import PriorityQueue


def merge_sorted_arrays(arrays: list[list], key: Callable = None, reverse=False):
    """
        Same as heapq.merge(*iterables, key=None, reverse=False)
        Time: O(NlogK) where N is all the elements in all arrays, K is the number of arrays
        Space: O(K) where K is priority queue size
        reverse = True for descending order
    """
    pq = PriorityQueue(min_heap=not reverse)
    for array_id, array in enumerate(arrays):
        if len(array) > 0:
            data = array[0] if key is None else key(array[0])
            pq.push((array_id, 0), data)
    while len(pq) > 0:
        array_id, index = pq.pop()
        yield arrays[array_id][index]
        index += 1
        if index < len(arrays[array_id]):
            data = arrays[array_id][index] if key is None else key(arrays[array_id][index])
            pq.push((array_id, index), data)
