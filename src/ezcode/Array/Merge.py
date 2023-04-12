from typing import Callable, Iterable
from ezcode.Heap.PriorityQueue import PriorityQueue


def merge_sorted_iterables(iterables: Iterable[Iterable], key: Callable = None, reverse=False):
    """
        Same as heapq.merge(*iterables, key=None, reverse=False)
        Time: O(NlogK) where N is all the elements in all arrays, K is the number of arrays
        Space: O(K) where K is priority queue size
        reverse = True for descending order
    """
    pq = PriorityQueue(reverse=reverse)
    for iterable in iterables:
        iterator = iter(iterable)
        data = next(iterator, None)
        if data is not None:
            pq.push(item=(iterator, data), priority=data if key is None else key(data))
    while len(pq) > 0:
        iterator, data = pq.pop()
        yield data
        data = next(iterator, None)
        if data is not None:
            pq.push(item=(iterator, data), priority=data if key is None else key(data))
