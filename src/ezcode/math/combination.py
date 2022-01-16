from ezcode.math.permutation import permutation_size


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


# def combinations(selection_size: int, items: list):
#     def _combinations(selection_size: int, items: list, current_size: int, selected_indices: set(), result):
#         if current_size == selection_size:
#             result.append(combination.copy())
#             return
#         selected_items = set()
#         for i in range(item_i, len(items)):
#             if items[i] not in selected_items:
#                 selected_items.add(items[i])
#                 combination.append(items[i])
#                 _combinations(items, item_i + 1, combination_size, combination, result)
#                 combination.pop()
#                 selected_items.remove(items[i])
#     
#     result = list()



# def all_combinations(items: list):
#     """ All subsets """
#     def _all_combinations(items, selection_size, combination, result):
#         if selection_size == len(items):
#             return
#         result.append(combination.copy())
