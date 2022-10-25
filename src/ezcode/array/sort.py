import random


def partition_with_first_item_as_pivot(array: list, start: int, end: int, reverse: bool = False):
    pivot, b = start, start + 1  # b point to the item larger than or equals to array[pivot].
    for e in range(start + 1, end + 1):
        if (not reverse and array[e] <= array[pivot]) or (reverse and array[pivot] <= array[e]):
            array[b], array[e] = array[e], array[b]  # swap(array, b, e)
            b += 1
    array[b - 1], array[pivot] = array[pivot], array[b - 1]  # swap(array, b - 1, pivot)
    return b - 1


def partition(array: list, start: int, end: int, pivot: int, reverse: bool = False):
    if pivot < start or pivot > end:
        raise ValueError(f"pivot {pivot} out of range [{start}, {end}]")
    array[start], array[pivot] = array[pivot], array[start]  # swap(array, start, pivot)
    return partition_with_first_item_as_pivot(array, start, end, reverse)


def partition_with_random_pivot(array: list, start: int, end: int, reverse: bool = False):
    pivot = random.randint(start, end)  # [start, end]
    return partition(array, start, end, pivot, reverse)


def quick_sort(array: list, start: int = None, end: int = None, reverse: bool = False):
    # inplace sort array[start:end]
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1
    if start < end:
        pivot_index = partition_with_random_pivot(array, start, end, reverse)
        quick_sort(array, start, pivot_index - 1, reverse)
        quick_sort(array, pivot_index + 1, end, reverse)






