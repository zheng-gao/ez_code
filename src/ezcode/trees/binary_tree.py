import random

from ezcode.trees.algorithms import *
from ezcode.trees.const import *
from ezcode.trees.printer import *


class BinaryTree(object):
    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, root=None, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
        self.root = root
        self.data_name=data_name
        self.left_name=left_name
        self.right_name=right_name

    def new_node(self, data):
        node = self.FakeNode()
        node.__dict__ = {self.data_name: data, self.left_name: None, self.right_name: None}
        return node
    
    def node_data(self, node):
        return node.__dict__[self.data_name]

    def print(self,
        left_wing: str = LEFT_WING, right_wing: str = RIGHT_WING,
        left_wing_head: str = LEFT_WING_HEAD, right_wing_head: str = RIGHT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL, right_wing_tail: str = RIGHT_WING_TAIL
    ):
        BinaryTreePrinter(
            data_name=self.data_name, left_name=self.left_name, right_name=self.right_name,
            left_wing=left_wing, right_wing=right_wing,
            left_wing_head=left_wing_head, right_wing_head=right_wing_head,
            left_wing_tail=left_wing_tail, right_wing_tail=right_wing_tail
        ).print(self.root)

    def depth(self):
        return find_depth(self.root, self.left_name, self.right_name)

    def is_balanced(self):
        return is_balanced(self.root, self.left_name, self.right_name)[0]

    def traversal(self, mode="pre-order"):
        result = list()
        if mode not in ["pre-order", "in-order", "post-order"]:
            raise ValueError(f"mode = \"{mode}\" is not supported, please choose from [\"pre-order\", \"in-order\", \"post-order\"]")
        elif mode == "pre-order":
            pre_order(self.root, result, self.data_name, self.left_name, self.right_name)
        elif mode == "in-order":
            in_order(self.root, result, self.data_name, self.left_name, self.right_name)
        elif mode == "post-order":
            post_order(self.root, result, self.data_name, self.left_name, self.right_name)
        return result

    def subtree(self, mode="sum-min"):
        if mode not in ["sum-min", "sum-max", "avg-min", "avg-max"]:
            raise ValueError(f"mode = \"{mode}\" is not supported, please choose from [\"sum-min\", \"sum-max\", \"avg-min\", \"avg-max\"]")
        elif mode == "sum-min":
            return subtree_sum_extremum(self.root, min, self.data_name, self.left_name, self.right_name)[0]
        elif mode == "sum-max":
            return subtree_sum_extremum(self.root, max, self.data_name, self.left_name, self.right_name)[0]
        elif mode == "avg-min":
            return subtree_avg_extremum(self.root, min, self.data_name, self.left_name, self.right_name)[0]
        else:
            return subtree_avg_extremum(self.root, max, self.data_name, self.left_name, self.right_name)[0]

    def lowest_common_ancestor(self, nodes):
        if not nodes:
            return None
        if len(nodes) == 1:
            return lowest_common_ancestor(self.root, node[0], None, self.data_name, self.left_name, self.right_name)
        else:
            ancestor = nodes[0]
            for node in nodes[1:]:
                ancestor = lowest_common_ancestor(self.root, ancestor, node, self.data_name, self.left_name, self.right_name)
            return ancestor

    def max_path_sum(self):
        return max_path_sum(self.root, self.data_name, self.left_name, self.right_name)[0]


class RandomBinaryTree(BinaryTree):
    def __init__(self,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME,
        size: int = 0, lower_bound: int = 0, upper_bound: int = 0
    ):
        super(RandomBinaryTree, self).__init__(None, data_name, left_name, right_name)
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.make_tree()

    def add_node(self, data):
        def _add_node(node, data):
            if random.randint(0, 1) == 0:
                if node.__dict__[self.left_name] is None:
                    node.__dict__[self.left_name] = self.new_node(data)
                else:
                    _add_node(node.__dict__[self.left_name], data)
            else:
                if node.__dict__[self.right_name] is None:
                    node.__dict__[self.right_name] = self.new_node(data)
                else:
                    _add_node(node.__dict__[self.right_name], data)

        if self.root is None:
            self.root = self.new_node(data)
        else:
            _add_node(self.root, data)

    def make_tree(self):
        self.root = None
        for _ in range(self.size):
            self.add_node(random.randint(self.lower_bound, self.upper_bound))
