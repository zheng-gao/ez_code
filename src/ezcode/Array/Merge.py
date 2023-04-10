from ezcode.Heap.PriorityQueue import PriorityQueue


def merge_sorted_arrays(arrays: list[list], reverse=False):
    """
        Same as heapq.merge(*iterables, key=None, reverse=False)
        Time: O(NlogK) where N is all the elements in all arrays, K is the number of arrays
        Space: O(K) where K is priority queue size
        reverse = True for descending order
    """
    pq = PriorityQueue(min_heap=not reverse)
    for array_id, array in enumerate(arrays):
        if len(array) > 0:
            pq.push((array_id, 0), array[0])
    while len(pq) > 0:
        item, priority = pq.pop(with_priority=True)
        array_id, next_index = item[0], item[1] + 1
        yield priority
        if next_index < len(arrays[array_id]):
            pq.push((array_id, next_index), arrays[array_id][next_index])
