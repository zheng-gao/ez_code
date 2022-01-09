import sys

from eztree.utils.const import DATA_NAME, LEFT_NAME, RIGHT_NAME


def pre_order(root, result: list, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is not None:
        result.append(root.__dict__[data_name])
        pre_order(root.__dict__[left_name], result, data_name, left_name, right_name)
        pre_order(root.__dict__[right_name], result, data_name, left_name, right_name)


def in_order(root, result: list, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is not None:
        pre_order(root.__dict__[left_name], result, data_name, left_name, right_name)
        result.append(root.__dict__[data_name])
        pre_order(root.__dict__[right_name], result, data_name, left_name, right_name)


def post_order(root, result: list, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is not None:
        pre_order(root.__dict__[left_name], result, data_name, left_name, right_name)
        pre_order(root.__dict__[right_name], result, data_name, left_name, right_name)
        result.append(root.__dict__[data_name])


def subtree_sum_extremum(root, extremum_func, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is None:
        return 0, 0
    left_sum_extremum, left_sum = subtree_sum_extremum(root.__dict__[left_name], extremum_func, data_name, left_name, right_name)
    right_sum_extremum, right_sum = subtree_sum_extremum(root.__dict__[right_name], extremum_func, data_name, left_name, right_name)
    my_sum = left_sum + right_sum + root.__dict__[data_name]
    return extremum_func(my_sum, left_sum_extremum, right_sum_extremum), my_sum


def subtree_avg_extremum(root, extremum_func, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is None:
        return 0, 0, 0
    left_avg_extremum, left_sum, left_size = subtree_avg_extremum(root.__dict__[left_name], extremum_func, data_name, left_name, right_name)
    right_avg_extremum, right_sum, right_size = subtree_avg_extremum(root.__dict__[right_name], extremum_func, data_name, left_name, right_name)
    my_sum = left_sum + right_sum + root.__dict__[data_name]
    my_size = left_size + right_size + 1
    my_average = my_sum / my_size
    return extremum_func(my_average, left_avg_extremum, right_avg_extremum), my_sum, my_size


def lowest_common_ancestor(root, node_1, node_2, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is None or root == node_1 or root == node_2:
        return root
    left_ancestor = lowest_common_ancestor(root.__dict__[left_name], node_1, node_2, data_name, left_name, right_name)
    right_ancestor = lowest_common_ancestor(root.__dict__[right_name], node_1, node_2, data_name, left_name, right_name)
    if left_ancestor is None and right_ancestor is None:
        return None
    if left_ancestor is not None and right_ancestor is not None:
        return root
    return left_ancestor if left_ancestor is not None else right_ancestor


def find_depth(root, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME) -> int:
    if root is None:
        return 0
    left_depth = find_depth(root.__dict__[left_name], left_name, right_name)
    right_depth = find_depth(root.__dict__[right_name], left_name, right_name)
    return max(left_depth, right_depth) + 1

def is_balanced(root, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME) -> (bool, int):
    if root is None:
        return True, 0
    left_balanced, left_depth = is_balanced(root.__dict__[left_name], left_name, right_name)
    right_balanced, right_depth = is_balanced(root.__dict__[right_name], left_name, right_name)
    return left_balanced and right_balanced and abs(left_depth - right_depth) <= 1, max(left_depth, right_depth) + 1


def max_path_sum(root, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
    if root is None:
        return -sys.maxsize, 0  # path sum max，max half + node value
    left_max, l_half = max_path_sum(root.__dict__[left_name], data_name, left_name, right_name)  # left path max, left non-negative max half
    right_max, r_half = max_path_sum(root.__dict__[right_name], data_name, left_name, right_name)  # right path max, right non-negative max half
    return max(left_max, right_max, root.__dict__[data_name] + l_half + r_half), max(root.__dict__[data_name] + max(l_half, r_half), 0)
