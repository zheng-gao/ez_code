from __future__ import annotations

import random

from collections import deque

from ezcode.tree.const import *
from ezcode.tree.algorithm import BinaryTreeAlgorithm
from ezcode.tree.printer import BinaryTreePrinter


class BinaryTree(object):

    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, root=None, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME):
        self.root = root
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.algorithm = BinaryTreeAlgorithm(data_name, left_name, right_name)

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
        return self.algorithm.depth(self.root)

    def is_balanced(self) -> bool:
        return self.algorithm.is_balanced(self.root)[0]

    def traversal(self, mode="pre-order"):
        result = list()
        if mode not in ["pre-order", "in-order", "post-order"]:
            raise ValueError(f"mode = \"{mode}\" is not supported, please choose from [\"pre-order\", \"in-order\", \"post-order\"]")
        elif mode == "pre-order":
            self.algorithm.pre_order(self.root, result)
        elif mode == "in-order":
            self.algorithm.in_order(self.root, result)
        elif mode == "post-order":
            self.algorithm.post_order(self.root, result)
        return result

    def subtree(self, mode="sum-min"):
        if mode not in ["sum-min", "sum-max", "avg-min", "avg-max"]:
            raise ValueError(f"mode = \"{mode}\" is not supported, please choose from [\"sum-min\", \"sum-max\", \"avg-min\", \"avg-max\"]")
        elif mode == "sum-min":
            return self.algorithm.subtree_sum_extremum(self.root, min)[0]
        elif mode == "sum-max":
            return self.algorithm.subtree_sum_extremum(self.root, max)[0]
        elif mode == "avg-min":
            return self.algorithm.subtree_avg_extremum(self.root, min)[0]
        else:
            return self.algorithm.subtree_avg_extremum(self.root, max)[0]

    def lowest_common_ancestor(self, nodes):
        if not nodes:
            return None
        if len(nodes) == 1:
            return nodes[0]
        ancestor = nodes[0]
        for node in nodes[1:]:
            ancestor = self.algorithm.lowest_common_ancestor(self.root, ancestor, node)
        return ancestor

    def max_path_sum(self):
        return self.algorithm.max_path_sum(self.root)[0]

    def serialize(self, delimiter: str = ",") -> str:
        if not self.root:
            return ""
        sequence = [self.root.__dict__[self.data_name]]
        queue = deque([self.root])
        while len(queue) > 0:
            node = queue.popleft()
            if node:
                queue.append(node.__dict__[self.left_name])
                queue.append(node.__dict__[self.right_name])
                if not node.__dict__[self.left_name]:
                    sequence.append(None)
                else:
                    sequence.append(node.__dict__[self.left_name].__dict__[self.data_name])
                if not node.__dict__[self.right_name]:
                    sequence.append(None)
                else:
                    sequence.append(node.__dict__[self.right_name].__dict__[self.data_name])
        return delimiter.join([str(x) for x in sequence])

    def deserialize(self, formatter, string: str, delimiter: str = ","):
        sequence = string.split(delimiter)
        if not sequence or not sequence[0]:
            return None
        root = self.new_node(formatter(sequence[0]))
        index, queue = 1, deque([root])
        while len(queue) > 0:
            node = queue.popleft()
            if node:
                left = self.new_node(formatter(sequence[index])) if sequence[index] != "None" else None
                right = self.new_node(formatter(sequence[index + 1])) if sequence[index + 1] != "None" else None
                queue.append(left)
                queue.append(right)
                node.__dict__[self.left_name], node.__dict__[self.right_name] = left, right
                index += 2
        return BinaryTree(root, self.data_name, self.left_name, self.right_name)

    def is_copied(self, tree: BinaryTree) -> bool:
        return self.algorithm.is_copied(self.root, tree.root)

    def copy(self) -> BinaryTree:
        if self.root is None:
            return BinaryTree(None, self.data_name, self.left_name, self.right_name)
        self_queue = deque([self.root])
        other_root = self.new_node(data=self.root.__dict__[self.data_name])
        other_queue = deque([other_root])
        while len(self_queue) > 0:
            self_node = self_queue.popleft()
            other_node = other_queue.popleft()
            if self_node:
                self_queue.append(self_node.__dict__[self.left_name])
                self_queue.append(self_node.__dict__[self.right_name])
                if self_node.__dict__[self.left_name]:
                    other_node.__dict__[self.left_name] = self.new_node(data=self_node.__dict__[self.left_name].__dict__[self.data_name])
                if self_node.__dict__[self.right_name]:
                    other_node.__dict__[self.right_name] = self.new_node(data=self_node.__dict__[self.right_name].__dict__[self.data_name])
                other_queue.append(other_node.__dict__[self.left_name])
                other_queue.append(other_node.__dict__[self.right_name])
        return BinaryTree(other_root, self.data_name, self.left_name, self.right_name)
        

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
