from ezcode.array.utils import swap


def selected_permutation_size(total_size: int, selection_size: int) -> int:
    """ Not for duplicate items: P(N,r) = N!/(N-r)! """
    if selection_size > total_size:
        raise ValueError(f"selection_size:{selection_size} cannot be greater than total_size:{total_size}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = 1
    for i in range(total_size - selection_size + 1, total_size + 1):
        result *= i
    return result


def selected_permutations(selection_size: int, items: list) -> list:

    def _selected_permutations(selection_size: int, items: list, selected_indices: set(), permutation: list, result: list):
        if len(permutation) == selection_size:
            result.append(permutation.copy())
            return
        selected_items = set()
        for i in range(len(items)):
            if i not in selected_indices:
                if items[i] not in selected_items: # check for duplicate items
                    selected_items.add(items[i])   #
                    selected_indices.add(i)
                    permutation.append(items[i])
                    _selected_permutations(selection_size, items, selected_indices, permutation, result)
                    permutation.pop()
                    selected_indices.remove(i)

    if items is None:
        return None
    if selection_size > len(items):
        raise ValueError(f"selection_size:{selection_size} cannot be greater than len(items):{len(items)}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = list()
    _selected_permutations(selection_size, items, set(), list(), result)
    return result


def complete_permutations(items: list) -> list:

    """ Equals to selected_permutations(len(items, items)) """
    def _complete_permutations(items: list, current_index, result: list):
        if current_index == len(items) - 1:
            result.append(items.copy())
            return
        selected_items = set()
        for next_index in range(current_index, len(items)):
            if items[next_index] not in selected_items:  # check for duplicate items
                selected_items.add(items[next_index])    # 
                swap(items, current_index, next_index)
                _complete_permutations(items, current_index + 1, result)
                swap(items, current_index, next_index)

    if items is None:
        return None
    if len(items) == 0:
        return [[]]
    result = list()
    _complete_permutations(items, 0, result)
    return result

