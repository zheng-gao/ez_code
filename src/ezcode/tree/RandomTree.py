from random import randint

from ezcode.Tree.BinaryTree import BinaryTree


class RandomTree(BinaryTree):
    def __init__(self, size: int = 0, lower_bound: int = 0, upper_bound: int = 0):
        super().__init__(root=None, data_name="data", left_name="left", right_name="right")
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.make_tree()

    def insert(self, data):
        def add_node_helper(node, data):
            if randint(0, 1) == 0:
                if node.left is None:
                    node.left = self.new_node(data)
                else:
                    add_node_helper(node.left, data)
            else:
                if node.right is None:
                    node.right = self.new_node(data)
                else:
                    add_node_helper(node.right, data)

        if self.root is None:
            self.root = self.new_node(data)
        else:
            add_node_helper(self.root, data)

    def build_tree(self):
        self.root = None
        for _ in range(self.size):
            self.insert(randint(self.lower_bound, self.upper_bound))
