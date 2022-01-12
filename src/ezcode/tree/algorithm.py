import sys

from ezcode.tree.const import DATA_NAME, LEFT_NAME, RIGHT_NAME


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
            self.pre_order(root.__dict__[self.left_name], result)
            result.append(root.__dict__[self.data_name])
            self.pre_order(root.__dict__[self.right_name], result)
    
    def post_order(self, root, result: list):
        if root is not None:
            self.pre_order(root.__dict__[self.left_name], result)
            self.pre_order(root.__dict__[self.right_name], result)
            result.append(root.__dict__[self.data_name])

    def depth(self, root):
        if root is None:
            return 0
        return max(self.depth(root.__dict__[self.left_name]), self.depth(root.__dict__[self.right_name])) + 1

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
    
    def lowest_common_ancestor(self, root, node_1, node_2):
        if root is None or root == node_1 or root == node_2:
            return root
        left_ancestor = self.lowest_common_ancestor(root.__dict__[self.left_name], node_1, node_2)
        right_ancestor = self.lowest_common_ancestor(root.__dict__[self.right_name], node_1, node_2)
        if left_ancestor is None and right_ancestor is None:
            return None
        if left_ancestor is not None and right_ancestor is not None:
            return root
        return left_ancestor if left_ancestor is not None else right_ancestor

    def is_balanced(self, root) -> (bool, int):
        if root is None:
            return True, 0
        left_balanced, left_depth = self.is_balanced(root.__dict__[self.left_name])
        right_balanced, right_depth = self.is_balanced(root.__dict__[self.right_name])
        return left_balanced and right_balanced and abs(left_depth - right_depth) <= 1, max(left_depth, right_depth) + 1
    
    def is_copied(self, root_1, root_2):
        if not root_1 and not root_2:
            return True
        if not root_1 or not root_2:
            return False
        if root_1.__dict__[self.data_name] != root_2.__dict__[self.data_name]:
            return False
        return self.is_copied(root_1.__dict__[self.left_name], root_2.__dict__[self.left_name]) and \
               self.is_copied(root_1.__dict__[self.right_name], root_2.__dict__[self.right_name])
    
    def max_path_sum(self, root):
        if root is None:
            return -sys.maxsize, 0  # path sum max，max half + node value
        left_max, l_half = self.max_path_sum(root.__dict__[self.left_name])  # left path max, left non-negative max half
        right_max, r_half = self.max_path_sum(root.__dict__[self.right_name])  # right path max, right non-negative max half
        return max(left_max, right_max, root.__dict__[self.data_name] + l_half + r_half), \
               max(root.__dict__[self.data_name] + max(l_half, r_half), 0)





    