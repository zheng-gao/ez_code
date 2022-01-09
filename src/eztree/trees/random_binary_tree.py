import random

from eztree.utils.const import DATA_NAME, LEFT_NAME, RIGHT_NAME
from eztree.trees.binary_tree import BinaryTree


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
