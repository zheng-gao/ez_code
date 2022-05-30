

def binary_search_subarray(array, begin: int, end: int, target, is_ascending=True, has_duplicates=False, is_left_most=True) -> int:
    if not array:
        return None
    while begin < end:
        mid = begin + (end - begin) // 2
        if not is_left_most and (end - begin) % 2 == 1:
            mid += 1
        if (is_ascending and target < array[mid]) or (not is_ascending and target > array[mid]):
            end = mid - 1
        elif (is_ascending and target > array[mid]) or (not is_ascending and target < array[mid]):
            begin = mid + 1
        else:
            if has_duplicates:
                if is_left_most:
                    end = mid
                else:  # right_most
                    begin = mid
            else:
                return mid
    return begin if array[begin] == target else None


def binary_search(array, target, is_ascending=True, has_duplicates=False, is_left_most=True) -> int:
    """ is_left_most is used when the array has duplicate entries """
    if not array:
        return None
    return binary_search_subarray(array, 0, len(array) - 1, target, is_ascending, has_duplicates, is_left_most)


def binary_search_subarray_exclusive_boundery(array, begin, end, target, is_ascending=True, is_smaller=True):
    if not array:
        return None
    if is_ascending:
        if target > array[end]:
            return end if is_smaller else None
        if target < array[begin]:
            return None if is_smaller else begin
    else:
        if target > array[begin]:
            return begin if is_smaller else None
        if target < array[end]:
            return None if is_smaller else end
    exclusive_boundery_index = None
    while begin <= end:
        mid = begin + (end - begin) // 2
        if is_ascending:
            if is_smaller:
                if target <= array[mid]:
                    end = mid - 1
                else:
                    exclusive_boundery_index = mid
                    begin = mid + 1
            else:
                if target >= array[mid]:
                    begin = mid + 1
                else:
                    exclusive_boundery_index = mid
                    end = mid - 1
        else:
            if is_smaller:
                if target <= array[mid]:
                    begin = mid + 1
                else:
                    exclusive_boundery_index = mid
                    end = mid - 1
            else:
                if target >= array[mid]:
                    end = mid - 1
                else:
                    exclusive_boundery_index = mid
                    begin = mid + 1
    return exclusive_boundery_index


def binary_search_exclusive_boundery(array, target, is_ascending=True, is_smaller=True):
    return binary_search_subarray_exclusive_boundery(array, 0, len(array) - 1, target, is_ascending, is_smaller)


def binary_search_range(array, target, is_ascending=True, is_inclusive=True) -> (int, int):
    if is_inclusive:
        lower_bound = binary_search(array, target, is_ascending, has_duplicates=True, is_left_most=True)
        upper_bound = binary_search(array, target, is_ascending, has_duplicates=True, is_left_most=False)
    else:
        if is_ascending:
            lower_bound = binary_search_exclusive_boundery(array, target, is_ascending, is_smaller=True)
            upper_bound = binary_search_exclusive_boundery(array, target, is_ascending, is_smaller=False)
        else:
            lower_bound = binary_search_exclusive_boundery(array, target, is_ascending, is_smaller=False)
            upper_bound = binary_search_exclusive_boundery(array, target, is_ascending, is_smaller=True)
    return lower_bound, upper_bound





