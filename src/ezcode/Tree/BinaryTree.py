from __future__ import annotations

from collections import deque
from random import randint
from typing import Callable, Iterable

from ezcode.Tree import (
    DATA_NAME,
    LEFT_NAME,
    RIGHT_NAME,
    LEFT_WING,
    RIGHT_WING,
    LEFT_WING_HEAD,
    RIGHT_WING_HEAD,
    LEFT_WING_TAIL,
    RIGHT_WING_TAIL
)
from ezcode.Tree.BinaryTreeAlgorithm import BinaryTreeAlgorithm
from ezcode.Tree.BinaryTreeIterator import BinaryTreeIterator
from ezcode.Tree.BinaryTreePrinter import BinaryTreePrinter


class BinaryTree(object):

    class BinaryTreeNode(object):
        def __init__(self):
            pass

        def match(self, node) -> bool:
            return all(attribute in self.__dict__.keys() for attribute in node.__dict__.keys())

    def __init__(self, init_data: Iterable = None, root=None, root_copy=None,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME,
        iterator_mode: BinaryTreeIterator.Mode = BinaryTreeIterator.Mode.DFS,
        iterator_is_left_first: bool = True,
        algorithm: BinaryTreeAlgorithm = None
    ):
        self.root, self.size = root, 0
        self.data_name, self.left_name, self.right_name = data_name, left_name, right_name
        self.iterator_mode, self.iterator_is_left_first = iterator_mode, iterator_is_left_first
        self.algorithm = algorithm if algorithm is not None else BinaryTreeAlgorithm(data_name, left_name, right_name)
        if root is not None:  # Any change on this tree will affect the original tree on the root
            self._size()
        elif root_copy is not None:
            self.root, self.size = self.copy_tree(root_copy)
        if init_data is not None:
            for data in init_data:
                self.insert(data)

    def __len__(self):
        return self.size

    def _size(self):  # recalculate the size
        self.size = 0
        for _ in iter(self):
            self.size += 1

    def __iter__(self):
        return BinaryTreeIterator(
            node=self.root,
            mode=self.iterator_mode,
            is_left_first=self.iterator_is_left_first,
            data_name=self.data_name,
            left_name=self.left_name,
            right_name=self.right_name
        )  # New iterator every time instead of keeping an iterator instance since self.root might change overtime

    def __reversed__(self):
        return BinaryTreeIterator(
            node=self.root,
            mode=self.iterator_mode,
            is_left_first=(not self.iterator_is_left_first),
            data_name=self.data_name,
            left_name=self.left_name,
            right_name=self.right_name
        )

    def __contains__(self, data) -> bool:
        return any(data == d for d in iter(self))

    def __str__(self) -> str:
        return self.to_string()

    def new_node(self, data=None, left=None, right=None):
        node = BinaryTree.BinaryTreeNode()
        node.__dict__ = {self.data_name: data, self.left_name: left, self.right_name: right}
        return node

    @staticmethod
    def copy_node(node):
        node_copy = BinaryTree.BinaryTreeNode()
        for key, value in node.__dict__.items():
            node_copy.__dict__[key] = value
        return node_copy

    def node_to_string(self, node) -> str:
        return str(self.get_data(node))

    def validate(self) -> bool:
        raise NotImplementedError

    def get_data(self, node):
        return node.__dict__[self.data_name]

    def set_data(self, node, data):
        node.__dict__[self.data_name] = data

    def get_left(self, node):
        return node.__dict__[self.left_name]

    def set_left(self, node, left):
        node.__dict__[self.left_name] = left

    def get_right(self, node):
        return node.__dict__[self.right_name]

    def set_right(self, node, right):
        node.__dict__[self.right_name] = right

    def insert(self, data):
        """ The nodes with same depth have the same probability """
        def _insert_random_node(node, data):
            if randint(0, 1) == 0:
                left = self.get_left(node)
                if left is None:
                    self.set_left(node, self.new_node(data))
                else:
                    _insert_random_node(left, data)
            else:
                right = self.get_right(node)
                if right is None:
                    self.set_right(node, self.new_node(data))
                else:
                    _insert_random_node(right, data)

        if self.root is None:
            self.root = self.new_node(data)
        else:
            _insert_random_node(self.root, data)
        self.size += 1

    def remove(self, data):
        raise NotImplementedError

    def remove_node(self, node):
        raise NotImplementedError

    def get_left_most(self, node):
        """ O(logN) """
        if node is None:
            raise ValueError(f"Invalid node: {node}")
        while self.get_left(node) is not None:
            node = self.get_left(node)
        return node

    def get_right_most(self, node):
        """ O(logN) """
        if node is None:
            raise ValueError(f"Invalid node: {node}")
        while self.get_right(node) is not None:
            node = self.get_right(node)
        return node

    def get_depth(self, node) -> int:
        """
            count nodes on the path from root to the given node
            this method should be overridden if the node has a parent pointer
        """
        def _get_depth(root, node, depth):
            if root is None or root == node:
                return root, depth
            left, right = self.get_left(root), self.get_right(root)
            if left is not None:
                root, new_depth = _get_depth(left, node, depth + 1)
                if root == node:
                    return root, new_depth
            if right is not None:
                root, new_depth = _get_depth(right, node, depth + 1)
                if root == node:
                    return root, new_depth
            return None, 0

        if node is None:
            return 0
        root, depth = _get_depth(self.root, node, 1)
        return depth if root == node else 0

    def get_height(self, node) -> int:
        """ count nodes on the path from the given node to its furthest leave """
        if node is None:
            return 0
        return max(self.get_height(self.get_left(node)), self.get_height(self.get_right(node))) + 1

    def print(self,
        left_wing: str = LEFT_WING,
        left_wing_head: str = LEFT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL,
        right_wing: str = RIGHT_WING,
        right_wing_head: str = RIGHT_WING_HEAD,
        right_wing_tail: str = RIGHT_WING_TAIL,
        node_to_string: Callable = None
    ):
        print(
            "\n" + self.to_string(
                left_wing=left_wing,
                left_wing_head=left_wing_head,
                left_wing_tail=left_wing_tail,
                right_wing=right_wing,
                right_wing_head=right_wing_head,
                right_wing_tail=right_wing_tail,
                node_to_string=node_to_string
            )
        )

    def to_string(self,
        left_wing: str = LEFT_WING,
        left_wing_head: str = LEFT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL,
        right_wing: str = RIGHT_WING,
        right_wing_head: str = RIGHT_WING_HEAD,
        right_wing_tail: str = RIGHT_WING_TAIL,
        node_to_string: Callable = None
    ):
        return BinaryTreePrinter(
            data_name=self.data_name,
            left_name=self.left_name,
            right_name=self.right_name,
            left_wing=left_wing,
            left_wing_head=left_wing_head,
            left_wing_tail=left_wing_tail,
            right_wing=right_wing,
            right_wing_head=right_wing_head,
            right_wing_tail=right_wing_tail,
            node_to_string=self.node_to_string if node_to_string is None else node_to_string
        ).to_string(self.root)

    def clear(self):
        self.root = None

    def height(self):
        return self.get_height(self.root)

    def is_balanced(self) -> bool:
        return self.algorithm.is_balanced(self.root)[0]

    def traversal(self, mode="pre-order"):
        valid_mode = ["pre-order", "in-order", "post-order", "level-order"]
        result = list()
        if mode not in valid_mode:
            raise ValueError(f"mode \"{mode}\" is not supported, please choose from {valid_mode}")
        elif mode == "pre-order":
            self.algorithm.pre_order(self.root, result)
        elif mode == "in-order":
            self.algorithm.in_order(self.root, result)
        elif mode == "post-order":
            self.algorithm.post_order(self.root, result)
        elif mode == "level-order":
            self.algorithm.level_order(self.root, result)
        return result

    def subtree(self, mode="sum-min"):
        valid_mode = ["sum-min", "sum-max", "avg-min", "avg-max"]
        if mode not in valid_mode:
            raise ValueError(f"mode \"{mode}\" is not supported, please choose from {valid_mode}")
        elif mode == "sum-min":
            return self.algorithm.subtree_sum_extremum(self.root, min)[0]
        elif mode == "sum-max":
            return self.algorithm.subtree_sum_extremum(self.root, max)[0]
        elif mode == "avg-min":
            return self.algorithm.subtree_avg_extremum(self.root, min)[0]
        else:
            return self.algorithm.subtree_avg_extremum(self.root, max)[0]

    def lowest_common_ancestor(self, nodes):
        """
            this method should be overridden if the node has a parent pointer
            calculate depth_diff and move the deeper node up to the same depth, ...
        """
        def _lowest_common_ancestor(root, node_1, node_2):
            if root is None or root == node_1 or root == node_2:
                return root
            left_ancestor = _lowest_common_ancestor(self.get_left(root), node_1, node_2)
            right_ancestor = _lowest_common_ancestor(self.get_right(root), node_1, node_2)
            if left_ancestor is None and right_ancestor is None:
                return None
            if left_ancestor is not None and right_ancestor is not None:
                return root
            return left_ancestor if left_ancestor is not None else right_ancestor

        if nodes is None or self.root is None:
            return None
        if len(nodes) == 1:
            return nodes[0]
        ancestor = nodes[0]
        for node in nodes[1:]:
            ancestor = _lowest_common_ancestor(self.root, ancestor, node)
        return ancestor

    def max_path_sum(self):
        return self.algorithm.max_path_sum(self.root)[0]

    def serialize(self, delimiter: str = ",") -> str:
        if not self.root:
            return ""
        sequence = [self.get_data(self.root)]
        queue = deque([self.root])
        while len(queue) > 0:
            node = queue.popleft()
            if node:
                queue.append(self.get_left(node))
                queue.append(self.get_right(node))
                if not self.get_left(node):
                    sequence.append(None)
                else:
                    sequence.append(self.get_data(self.get_left(node)))
                if not self.get_right(node):
                    sequence.append(None)
                else:
                    sequence.append(self.get_data(self.get_right(node)))
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
                self.set_left(node, left)
                self.set_right(node, right)
                index += 2
        return BinaryTree(
            root=root, data_name=self.data_name,
            left_name=self.left_name, right_name=self.right_name
        )

    def __eq__(self, other) -> bool:
        """
            This method should be overridden by the subclass if the subclass node has different attributes
        """
        def _tree_equal(node_1, node_2):
            if node_1 is None and node_2 is None:
                return True
            if node_1 is None or node_2 is None:
                return False
            if self.get_data(node_1) != self.get_data(node_2):
                return False
            return _tree_equal(self.get_left(node_1), self.get_left(node_2)) and \
                _tree_equal(self.get_right(node_1), self.get_right(node_2))

        if isinstance(other, BinaryTree):
            return _tree_equal(self.root, other.root)
        return False

    def copy_tree(self, node):
        """
            This method should be overridden by the subclass
            Semi-deep copy: copy the tree structure but not the data
        """
        if node is None:
            return None, 0
        if not (self.root is None and self.new_node().match(node)) and not self.root.match(node):
            raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
        root_copy, size_copy = self.copy_node(node), 0
        queue, queue_copy = deque([node]), deque([root_copy])
        while len(queue) > 0:
            node = queue.popleft()
            node_copy = queue_copy.popleft()
            size_copy += 1
            left, right = self.get_left(node), self.get_right(node)
            if left is not None:
                left_copy = self.copy_node(left)
                self.set_left(node_copy, left=left_copy)
                queue.append(left)
                queue_copy.append(left_copy)
            if right is not None:
                right_copy = self.copy_node(right)
                self.set_right(node_copy, right=right_copy)
                queue.append(right)
                queue_copy.append(right_copy)
        return root_copy, size_copy

    def copy(self):
        """
            This method should be overridden by the subclass if the subclass node has different attributes
            Semi-deep copy: copy the tree structure but not the data
        """
        tree = self.__class__()
        tree.data_name = self.data_name
        tree.left_name = self.left_name
        tree.right_name = self.right_name
        tree.iterator_mode = self.iterator_mode
        tree.iterator_is_left_first = self.iterator_is_left_first,
        tree.algorithm = self.algorithm
        tree.root, tree.size = self.copy_tree(self.root)
        return tree


