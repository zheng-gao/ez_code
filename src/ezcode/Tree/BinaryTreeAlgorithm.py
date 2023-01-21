from collections import deque
from sys import maxsize

from ezcode.Tree import DATA_NAME, LEFT_NAME, RIGHT_NAME


class BinaryTreeAlgorithm:
    """ Recursion Helpers """
    def __init__(self, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name

    def pre_order(self, root, result: list):
        if root is not None:
            result.append(root.__dict__[self.data_name])
            self.pre_order(root.__dict__[self.left_name], result)
            self.pre_order(root.__dict__[self.right_name], result)

    def in_order(self, root, result: list):
        if root is not None:
            self.in_order(root.__dict__[self.left_name], result)
            result.append(root.__dict__[self.data_name])
            self.in_order(root.__dict__[self.right_name], result)

    def post_order(self, root, result: list):
        if root is not None:
            self.post_order(root.__dict__[self.left_name], result)
            self.post_order(root.__dict__[self.right_name], result)
            result.append(root.__dict__[self.data_name])

    def level_order(self, root, result: list = list(), left_most_nodes=False):
        if root is not None:
            queue = deque([root])
            current_level_node_count, next_level_node_count = 1, 0
            level_start, level = True, 0
            while len(queue) > 0:
                node = queue.popleft()
                if not left_most_nodes or level_start:
                    result.append(node.__dict__[self.data_name])
                    level_start = False
                current_level_node_count -= 1
                if node.__dict__[self.left_name]:
                    queue.append(node.__dict__[self.left_name])
                    next_level_node_count += 1
                if node.__dict__[self.right_name]:
                    queue.append(node.__dict__[self.right_name])
                    next_level_node_count += 1
                if current_level_node_count == 0:
                    current_level_node_count = next_level_node_count
                    next_level_node_count, level_start, level = 0, True, level + 1
            return level
        return 0

    def subtree_sum_extremum(self, root, extremum_func):
        if root is None:
            return 0, 0
        left_sum_extremum, left_sum = self.subtree_sum_extremum(root.__dict__[self.left_name], extremum_func)
        right_sum_extremum, right_sum = self.subtree_sum_extremum(root.__dict__[self.right_name], extremum_func)
        my_sum = left_sum + right_sum + root.__dict__[self.data_name]
        return extremum_func(my_sum, left_sum_extremum, right_sum_extremum), my_sum

    def subtree_avg_extremum(self, root, extremum_func):
        if root is None:
            return 0, 0, 0
        left_avg_extremum, left_sum, left_size = self.subtree_avg_extremum(root.__dict__[self.left_name], extremum_func)
        right_avg_extremum, right_sum, right_size = self.subtree_avg_extremum(root.__dict__[self.right_name], extremum_func)
        my_sum = left_sum + right_sum + root.__dict__[self.data_name]
        my_size = left_size + right_size + 1
        my_average = my_sum / my_size
        return extremum_func(my_average, left_avg_extremum, right_avg_extremum), my_sum, my_size

    def is_balanced(self, root) -> (bool, int):
        if root is None:
            return True, 0
        left_balanced, left_depth = self.is_balanced(root.__dict__[self.left_name])
        right_balanced, right_depth = self.is_balanced(root.__dict__[self.right_name])
        return left_balanced and right_balanced and abs(left_depth - right_depth) <= 1, max(left_depth, right_depth) + 1

    def max_path_sum(self, root):
        if root is None:
            return -maxsize, 0  # path sum max，max half + node value
        left_max, l_half = self.max_path_sum(root.__dict__[self.left_name])  # left path max, left non-negative max half
        right_max, r_half = self.max_path_sum(root.__dict__[self.right_name])  # right path max, right non-negative max half
        return max(left_max, right_max, root.__dict__[self.data_name] + l_half + r_half), max(root.__dict__[self.data_name] + max(l_half, r_half), 0)

    def remove_bst_node(self, root, data):
        if root is None:
            return None
        elif data < root.__dict__[self.data_name]:
            root.__dict__[self.left_name] = self.remove_bst_node(root.__dict__[self.left_name], data)
        elif data > root.__dict__[self.data_name]:
            root.__dict__[self.right_name] = self.remove_bst_node(root.__dict__[self.right_name], data)
        else:
            if root.__dict__[self.right_name] is None:
                return root.__dict__[self.left_name]
            else:
                left_most_parent, left_most = root, root.__dict__[self.right_name]
                while left_most is not None and left_most.__dict__[self.left_name] is not None:
                    left_most_parent = left_most
                    left_most = left_most.__dict__[self.left_name]
                root.__dict__[self.data_name] = left_most.__dict__[self.data_name]  # swap data then delete left_most
                side_name = self.right_name if left_most == root.__dict__[self.right_name] else self.left_name
                left_most_parent.__dict__[side_name] = left_most.__dict__[self.right_name]  # left_most only have the right child
        return root

