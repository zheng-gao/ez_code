from typing import Callable


def binary_search_range(
    target,
    array: list,
    is_ascending: bool = True,
    is_inclusive: bool = True,
    key: Callable = None
) -> tuple[int, int]:
    if is_inclusive:
        lower_bound = binary_search(target, array, is_ascending, has_duplicates=True, is_left_most=True, key=key)
        upper_bound = binary_search(target, array, is_ascending, has_duplicates=True, is_left_most=False, key=key)
    else:
        if is_ascending:
            lower_bound = exclusive_binary_search(target, array, is_ascending, is_smaller=True, key=key)
            upper_bound = exclusive_binary_search(target, array, is_ascending, is_smaller=False, key=key)
        else:
            lower_bound = exclusive_binary_search(target, array, is_ascending, is_smaller=False, key=key)
            upper_bound = exclusive_binary_search(target, array, is_ascending, is_smaller=True, key=key)
    return lower_bound, upper_bound


def binary_search(
    target,
    array: list,
    is_ascending: bool = True,
    has_duplicates: bool = False,
    is_left_most: bool = True,
    key: Callable = None
) -> int:
    """ is_left_most is used when the array has duplicate entries """
    if not array:
        return None
    return binary_search_subarray(target, array, 0, len(array) - 1, is_ascending, has_duplicates, is_left_most, key)


def binary_search_subarray(
    target,
    array: list,
    start: int,
    end: int,
    is_ascending: bool = True,
    has_duplicates: bool = False,
    is_left_most: bool = True,
    key: Callable = None
) -> int:
    if not array:
        return None
    while start < end:
        mid = start + (end - start + (0 if is_left_most else 1)) // 2
        array_mid = array[mid] if key is None else key(array[mid])
        if (is_ascending and target < array_mid) or (not is_ascending and array_mid < target):
            end = mid - 1
        elif (is_ascending and array_mid < target) or (not is_ascending and target < array_mid):
            start = mid + 1
        else:
            if has_duplicates:
                if is_left_most:
                    end = mid
                else:  # right_most
                    start = mid
            else:
                return mid
    array_start = array[start] if key is None else key(array[start])
    return start if array_start == target else None


def exclusive_binary_search(
    target,
    array: list,
    is_ascending: bool = True,
    is_smaller: bool = True,
    key: Callable = None
) -> int:
    return exclusive_binary_search_subarray(target, array, 0, len(array) - 1, is_ascending, is_smaller, key)


def exclusive_binary_search_subarray(
    target,
    array: list,
    start: int,
    end: int,
    is_ascending: bool = True,
    is_smaller: bool = True,
    key: Callable = None
) -> int:
    if not array:
        return None
    array_start = array[start] if key is None else key(array[start])
    array_end = array[end] if key is None else key(array[end])
    if is_ascending:
        if array_end < target:
            return end if is_smaller else None
        if target < array_start:
            return None if is_smaller else start
    else:
        if array_start < target:
            return start if is_smaller else None
        if target < array_end:
            return None if is_smaller else end
    exclusive_boundery_index = None
    while start <= end:
        mid = start + (end - start) // 2
        array_mid = array[mid] if key is None else key(array[mid])
        if is_ascending:
            if is_smaller:
                if array_mid < target:
                    exclusive_boundery_index = mid
                    start = mid + 1
                else:
                    end = mid - 1
            else:
                if target < array_mid:
                    exclusive_boundery_index = mid
                    end = mid - 1
                else:
                    start = mid + 1
        else:
            if is_smaller:
                if array_mid < target:
                    exclusive_boundery_index = mid
                    end = mid - 1
                else:
                    start = mid + 1
            else:
                if target < array_mid:
                    exclusive_boundery_index = mid
                    start = mid + 1
                else:
                    end = mid - 1
    return exclusive_boundery_index




