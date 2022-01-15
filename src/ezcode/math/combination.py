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


# def combinations(selection_size: int, items: list, ):
#     # Subset
#     pass
#     # def _combinations(items, item_i, combination_size, combination, result):
#     #     if ith_item == combination_size:
#     #         result.append(combination.copy())
#     #         return
#     #     for i in range(item_i, len(items)):
#     #         combination.append(items[i])
#     #         _combinations(items, item_i + 1, combination_size, combination, result)
#     #         combination.pop()
# 
# 
# def all_combinations(items: list):
#     """ All subsets """
#     def _all_combinations(items, selection_size, combination, result):
#         if selection_size == len(items):
#             return
#         result.append(combination.copy())
