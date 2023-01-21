from ezcode.Array.Utils import reverse
from ezcode.Array.Search import exclusive_binary_search_subarray


def permutation_size(total_size: int, selection_size: int) -> int:
    """ Not for duplicate items: P(N,r) = N!/(N-r)! """
    if selection_size > total_size:
        raise ValueError(f"selection_size:{selection_size} cannot be greater than total_size:{total_size}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = 1
    for i in range(total_size - selection_size + 1, total_size + 1):
        result *= i
    return result


def permutations(selection_size: int, items: list) -> list:
    def _permutations(selection_size: int, items: list, selected_indices: set(), permutation: list, result: list):
        if len(permutation) == selection_size:
            result.append(permutation.copy())
            return
        selected_items = set()
        for i in range(len(items)):
            if i not in selected_indices and items[i] not in selected_items:  # check for duplicate indices and duplicate items
                selected_indices.add(i)
                selected_items.add(items[i])
                permutation.append(items[i])
                _permutations(selection_size, items, selected_indices, permutation, result)
                permutation.pop()
                selected_indices.remove(i)

    if items is None:
        return None
    if selection_size > len(items):
        raise ValueError(f"selection_size:{selection_size} cannot be greater than len(items):{len(items)}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = list()
    _permutations(selection_size, items, set(), list(), result)
    return result


def next_lexicographic_permutation(items: list, copy=True) -> list:
    if copy:
        items = items.copy()
    start, end = -1, len(items) - 1
    for i in range(len(items) - 2, -1, -1):
        if items[i] < items[i + 1]:
            start = i
            break
    if start < 0:
        reverse(items)
    else:
        first_greater_from_end = exclusive_binary_search_subarray(items[start], items, start + 1, end, is_ascending=False, is_smaller=False)
        items[start], items[first_greater_from_end] = items[first_greater_from_end], items[start]  # swap
        reverse(items, start + 1, len(items) - 1)
    return items


def all_items_permutations(items: list) -> list:
    """ Equals to permutations(len(items, items)) """
    def _permutations_with_all_items(items: list, current_index, result: list):
        if current_index == len(items) - 1:
            result.append(items.copy())
            return
        selected_items = set()
        for next_index in range(current_index, len(items)):
            if items[next_index] not in selected_items:  # check for duplicate items
                selected_items.add(items[next_index])
                items[current_index], items[next_index] = items[next_index], items[current_index]  # swap current and next
                _permutations_with_all_items(items, current_index + 1, result)
                items[current_index], items[next_index] = items[next_index], items[current_index]  # swap current and next

    if items is None:
        return None
    if len(items) == 0:
        return [[]]
    result = list()
    _permutations_with_all_items(items, 0, result)
    return result



