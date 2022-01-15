from ezcode.array.utils import swap


def rotate(array, shifts, is_left_rotate):

    def _rotate(array, begin, end):
        while begin < end:
            swap(array, begin, end)
            begin += 1
            end -= 1

    if array:
        size = len(array)
        shifts = shifts % size if is_left_rotate else size - shifts % size
        if shifts > 0:
            _rotate(array, 0, shifts - 1)
            _rotate(array, shifts, size - 1)
            _rotate(array, 0, size - 1)


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


