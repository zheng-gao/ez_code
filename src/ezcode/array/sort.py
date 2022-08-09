import random


def partition_with_first_item_as_pivot(array: list, begin: int, end: int, reverse: bool = False):
    pivot, b = begin, begin + 1  # b point to the item larger than or equals to array[pivot].
    for e in range(begin + 1, end + 1):
        if (not reverse and array[e] <= array[pivot]) or (reverse and array[pivot] <= array[e]):
            array[b], array[e] = array[e], array[b]  # swap(array, b, e)
            b += 1
    array[b - 1], array[pivot] = array[pivot], array[b - 1]  # swap(array, b - 1, pivot)
    return b - 1


def partition(array: list, begin: int, end: int, pivot: int, reverse: bool = False):
    if pivot < begin or pivot > end:
        raise ValueError(f"pivot {pivot} out of range [{begin}, {end}]")
    array[begin], array[pivot] = array[pivot], array[begin]  # swap(array, begin, pivot)
    return partition_with_first_item_as_pivot(array, begin, end, reverse)


def partition_with_random_pivot(array: list, begin: int, end: int, reverse: bool = False):
    pivot = random.randint(begin, end)  # [begin, end]
    return partition(array, begin, end, pivot, reverse)


def quick_sort(array: list, begin: int = None, end: int = None, reverse: bool = False):
    # inplace sort array[begin:end]
    if begin is None:
        begin = 0
    if end is None:
        end = len(array) - 1
    if begin < end:
        pivot_index = partition_with_random_pivot(array, begin, end, reverse)
        quick_sort(array, begin, pivot_index - 1, reverse)
        quick_sort(array, pivot_index + 1, end, reverse)






