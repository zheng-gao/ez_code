import math


def _binary_search(array, begin: int, end: int, target, is_ascending=True, is_left_most=True):
    while begin < end:
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


def binary_search(array, target, is_ascending=True, is_left_most=True):
    """ is_left_most is used when the array has duplicate entries """
    if not array:
        return None
    return _binary_search(array, 0, len(array) - 1, target, is_ascending, is_left_most)


# def is_rotated_sorted_array(array, is_ascending=True) -> bool:
#     not_in_order = 0
#     for i in range(len(array) - 1):
#         if not_in_order > 0 and (is_ascending and array[i] > array[0]) or (not is_ascending and array[i] < array[0]):
#             return False
#         if (is_ascending and array[i] > array[i + 1]) or (not is_ascending and array[i] < array[i + 1]):
#             not_in_order += 1
#     if not_in_order == 1:
#         if is_ascending:
#             return array[len(array) - 1] <= array[0]
#         else:
#             return array[len(array) - 1] >= array[0]
#     else:
#         return not_in_order == 0
# 
# 
# def find_min_index_in_rotated_sorted_array(array, is_ascending=True):
#     begin, end = 0, len(array) - 1
#     while begin < end:
#         mid = begin + (end - begin) // 2;
#         if mid == begin:
#             return begin if array[begin] < array[end] else end
#         if is_ascending and array[mid] == array[end]:  # Handle the case with duplicates
#             end -= 1
#         elif not is_ascending and array[mid] == array[begin]:
#             begin += 1
#         elif (is_ascending and array[mid] < array[end]) or (not is_ascending and array[mid] > array[begin]):
#             end = mid
#         else:
#             begin = mid
#     return begin 
# 
# 
# def binary_search_rotated(array, target, is_ascending=True, is_left_most=True):
#     min_index = find_min_index_in_rotated_sorted_array(array, is_ascending)
#     if (is_ascending and min_index == 0) or (not is_ascending and min_index == len(array) - 1):
#         return binary_search(array, target, is_ascending, is_left_most)
#     if is_ascending:
#         if target >= array[0]:
#             return _binary_search(array, 0, min_index - 1, target, is_ascending, is_left_most)
#         else:
#             return _binary_search(array, min_index, len(array) - 1, target, is_ascending, is_left_most)
#     else:
#         if target <= array[0]: 
#             return _binary_search(array, 0, min_index, target, is_ascending, is_left_most)
#         else:
#             return _binary_search(array, min_index + 1, len(array) - 1, target, is_ascending, is_left_most)



