import random
from ezcode.array.utils import swap


def partition_with_first_item_as_pivot(array: list, begin: int, end: int):
    pivot, b = begin, begin + 1  # b point to the item larger than or equals to array[pivot].
    for e in range(begin + 1, end + 1):
        if array[e] <= array[pivot]:
            swap(array, b, e)
            b += 1
    swap(array, b - 1, pivot)
    return b - 1


def partition(array: list, begin: int, end: int, pivot: int):
    if pivot < begin or pivot > end:
        raise ValueError(f"pivot {pivot} out of range [{begin}, {end}]")
    swap(array, begin, pivot)
    return partition_with_first_item_as_pivot(array, begin, end)


def partition_with_random_pivot(array: list, begin: int, end: int):
    pivot = random.randint(begin, end)  # [begin, end]
    return partition(array, begin, end, pivot)


def quick_sort(array: list, begin: int = None, end: int = None):
    # inplace sort array[begin:end]
    if begin is None:
        begin = 0
    if end is None:
        end = len(array) - 1
    if(begin < end):
        pivot_index = partition_with_random_pivot(array, begin, end)
        quick_sort(array, begin, pivot_index - 1)
        quick_sort(array, pivot_index + 1, end)






