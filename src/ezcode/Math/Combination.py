from ezcode.Math.Permutation import permutation_size


def combination_size(total_size: int, selection_size: int) -> int:
    """ C(N,r) = C(N,N-r) = A(N,r)/r! = N!/[r! * (N-r)!] """
    if selection_size > total_size:
        raise ValueError(f"selection_size:{selection_size} cannot be greater than total_size:{total_size}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = permutation_size(total_size, selection_size)
    for i in range(1, selection_size + 1):
        result //= i
    return result


def combinations(selection_size: int, items: list):
    def _combinations(selection_size: int, items: list, start_index: int, combination: list, result: list):
        if len(combination) == selection_size:
            result.append(combination.copy())
            return
        selected_items = set()
        end_index = len(items) - (selection_size - len(combination))  # not enough indices left, terminate recursion early
        for i in range(start_index, end_index + 1):
            if items[i] not in selected_items:  # check for duplicate items
                selected_items.add(items[i])
                combination.append(items[i])
                _combinations(selection_size, items, i + 1, combination, result)
                combination.pop()

    if items is None:
        return None
    if selection_size > len(items):
        raise ValueError(f"selection_size:{selection_size} cannot be greater than len(items):{len(items)}")
    if selection_size < 0:
        raise ValueError(f"selection_size:{selection_size} cannot be negative")
    result = list()
    items.sort()  # for duplicate items
    _combinations(selection_size, items, 0, list(), result)
    return result


def all_subsets(items: list, has_duplicate=True):
    """ Equals to combinations(i, items) for i in range(len(items) + 1) """
    def _all_subsets_recursion(items: list, start_index: int, subset: list, result: list):
        if start_index > len(items):
            return
        result.append(subset.copy())
        selected_items = set()
        for i in range(start_index, len(items)):
            if items[i] not in selected_items:  # check for duplicate items
                selected_items.add(items[i])
                subset.append(items[i])
                _all_subsets_recursion(items, i + 1, subset, result)
                subset.pop()

    def _all_subsets_iteration(items: list, result: list):
        """ 2^N subsets, Not for duplicate items """
        number_range = 1 << len(items)
        for i in range(number_range):
            subset = list()
            for shift in range(len(items)):
                if ((i >> shift) & 1) == 1:
                    subset.append(items[shift])
            result.append(subset.copy())

    if items is None:
        return None
    result = list()
    if has_duplicate:
        items.sort()  # for duplicate items
        _all_subsets_recursion(items, 0, list(), result)
    else:
        _all_subsets_iteration(items, result)
    result.sort(key=lambda x: len(x))  # nice to have
    return result


