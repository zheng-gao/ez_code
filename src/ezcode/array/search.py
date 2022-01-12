import math


def binary_search(array, target, is_ascending=True, is_left_most=True):
    """ is_left_most is used when the array has duplicate entries """
    if not array:
        return None
    begin, end = 0, len(array) - 1
    while begin != end:
        mid = begin + (end - begin) / 2
        mid = math.floor(mid) if is_left_most else math.ceil(mid)
        if (is_ascending and target < array[mid]) or (not is_ascending and target > array[mid]):
            end = mid - 1
        elif (is_ascending and target > array[mid]) or (not is_ascending and target < array[mid]):
            begin = mid + 1
        else:
            if is_left_most:
                end = mid
            else:
                begin = mid
    return begin if array[begin] == target else None


def find_rotates(array, is_ascending=True):
    pass