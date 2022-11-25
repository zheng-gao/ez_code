from __future__ import annotations

import random

from collections import deque
from typing import Callable

from ezcode.tree.const import DATA_NAME, LEFT_NAME, RIGHT_NAME
from ezcode.tree.const import LEFT_WING, RIGHT_WING, LEFT_WING_HEAD, RIGHT_WING_HEAD, LEFT_WING_TAIL, RIGHT_WING_TAIL
from ezcode.tree.algorithm import BinaryTreeAlgorithm
from ezcode.tree.printer import BinaryTreePrinter


class BinaryTree(object):

    class BinaryTreeNode(object):
        def __init__(self):
            pass

    def __init__(self, root=None, data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME, algorithm: BinaryTreeAlgorithm = None):
        self.root = root
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        if algorithm is None:
            self.algorithm = BinaryTreeAlgorithm(data_name, left_name, right_name)

    def new_node(self, data, left_node=None, right_node=None):
        node = self.BinaryTreeNode()
        node.__dict__ = {self.data_name: data, self.left_name: left_node, self.right_name: right_node}
        return node

    def node_to_string(self, node):
        return str(self.get_data(node))

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

    def print(self,
        left_wing: str = LEFT_WING, right_wing: str = RIGHT_WING,
        left_wing_head: str = LEFT_WING_HEAD, right_wing_head: str = RIGHT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL, right_wing_tail: str = RIGHT_WING_TAIL,
        node_to_string: Callable = None
    ):
        BinaryTreePrinter(
            data_name=self.data_name, left_name=self.left_name, right_name=self.right_name,
            left_wing=left_wing, right_wing=right_wing,
            left_wing_head=left_wing_head, right_wing_head=right_wing_head,
            left_wing_tail=left_wing_tail, right_wing_tail=right_wing_tail,
            node_to_string=self.node_to_string if node_to_string is None else node_to_string
        ).print(self.root)

    def depth(self):
        return self.algorithm.depth(self.root)

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
        return BinaryTree(root, self.data_name, self.left_name, self.right_name)

    def is_copied(self, tree: BinaryTree) -> bool:
        return self.algorithm.is_copied(self.root, tree.root)

    def copy(self) -> BinaryTree:
        if self.root is None:
            return BinaryTree(None, self.data_name, self.left_name, self.right_name)
        self_queue = deque([self.root])
        other_root = self.new_node(data=self.get_data(self.root))
        other_queue = deque([other_root])
        while len(self_queue) > 0:
            self_node = self_queue.popleft()
            other_node = other_queue.popleft()
            if self_node:
                self_queue.append(self.get_left(self_node))
                self_queue.append(self.get_right(self_node))
                if self.get_left(self_node):
                    self.set_left(other_node, self.new_node(data=self.get_data(self.get_left(self_node))))
                if self.get_right(self_node):
                    self.set_right(other_node, self.new_node(data=self.get_data(self.get_right(self_node))))
                other_queue.append(self.get_left(other_node))
                other_queue.append(self.get_right(other_node))
        return BinaryTree(other_root, self.data_name, self.left_name, self.right_name)

    def delete_bst_node(self, data):
        # self.root = self.algorithm.delete_bst_node(self.root, data)
        parent, node = None, self.root
        while node is not None:
            if data < self.get_data(node):
                parent, node = node, self.get_left(node)
            elif data > self.get_data(node):
                parent, node = node, self.get_right(node)
            else:
                if self.get_right(node) is None:
                    left_child = self.get_left(node)
                    if parent is None:
                        self.root = left_child
                    elif node == self.get_left(parent):
                        self.set_left(parent, left_child)
                    else:  # node == self.get_right(parent)
                        self.set_right(parent, left_child)
                else:  # left_most only have the right child
                    left_most_parent, left_most = node, self.get_right(node)
                    while left_most is not None and self.get_left(left_most) is not None:
                        left_most_parent = left_most
                        left_most = self.get_left(left_most)
                    self.set_data(node, self.get_data(left_most))  # swap data then delete left_most
                    if left_most == self.get_right(node):
                        self.set_right(left_most_parent, right=self.get_right(left_most))
                    else:
                        self.set_left(left_most_parent, left=self.get_right(left_most))
                break

    def delete_bst_nodes(self, data_lower_bound, data_upper_bound):
        if data_upper_bound < data_lower_bound:
            raise ValueError(f"data_upper_bound {data_upper_bound} is smaller than data_lower_bound {data_lower_bound}")
        parent, node = None, self.root
        while node is not None:
            data = self.get_data(node)
            if data < data_lower_bound:
                parent, node = node, self.get_right(node)
            elif data_upper_bound < data:
                parent, node = node, self.get_left(node)
            else:
                if self.get_right(node) is None:
                    left_child = self.get_left(node)
                    if parent is None:
                        self.root = left_child
                    elif node == self.get_left(parent):
                        self.set_left(parent, left_child)
                    else:  # node == self.get_right(parent)
                        self.set_right(parent, left_child)
                    node = left_child
                else:  # left_most only have the right child
                    left_most_parent, left_most = node, self.get_right(node)
                    while left_most is not None and self.get_left(left_most) is not None:
                        left_most_parent = left_most
                        left_most = self.get_left(left_most)
                    self.set_data(node, self.get_data(left_most))  # swap data then delete left_most
                    if left_most == self.get_right(node):
                        self.set_right(left_most_parent, right=self.get_right(left_most))
                    else:
                        self.set_left(left_most_parent, left=self.get_right(left_most))


class RandomBinaryTree(BinaryTree):
    def __init__(self,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME,
        size: int = 0, lower_bound: int = 0, upper_bound: int = 0
    ):
        super().__init__(None, data_name, left_name, right_name)
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.make_tree()

    def add_node(self, data):
        def add_node_helper(node, data):
            if random.randint(0, 1) == 0:
                if self.get_left(node) is None:
                    self.set_left(node, self.new_node(data))
                else:
                    add_node_helper(self.get_left(node), data)
            else:
                if self.get_right(node) is None:
                    self.set_right(node, self.new_node(data))
                else:
                    add_node_helper(self.get_right(node), data)

        if self.root is None:
            self.root = self.new_node(data)
        else:
            add_node_helper(self.root, data)

    def build_tree(self):
        self.root = None
        for _ in range(self.size):
            self.add_node(random.randint(self.lower_bound, self.upper_bound))


class SegmentTree(BinaryTree):
    """
        Suitable for repeated queries
        Cannot add or delete items once the tree is built
    """
    def __init__(self,
        merge: Callable = lambda x, y: x + y, data_list: list = None,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME
    ):
        super().__init__(None, data_name, left_name, right_name)
        self.merge = merge  # sum, max, min, gcd or lambda x, y: ...
        if data_list is not None:
            self.build_tree(data_list=data_list)

    def new_node(self, start: int, end: int, data, left_node=None, right_node=None):
        node = super().new_node(data, left_node, right_node)
        node.__dict__["start"] = start
        node.__dict__["end"] = end
        return node

    def node_to_string(self, node):
        return f"[{node.start},{node.end}]:" + str(self.get_data(node))

    def build_tree(self, data_list: list):
        """ Time: O(N), Space: O(N) """
        def build_tree_helper(start: int, end: int):
            if start == end:
                return self.new_node(start, end, data_list[start])
            mid = start + (end - start) // 2
            left_node = build_tree_helper(start, mid)  # left include mid
            right_node = build_tree_helper(mid + 1, end)
            new_data = self.merge(self.get_data(left_node), self.get_data(right_node))
            return self.new_node(start, end, new_data, left_node, right_node)

        self.root = build_tree_helper(0, len(data_list) - 1)

    def update(self, index: int, data):
        """ Time: O(logN) """
        def update_helper(node, index: int, data):
            if node.start == node.end == index:
                self.set_data(node, data)
                return
            mid = node.start + (node.end - node.start) // 2
            if index <= mid:  # left include mid
                update_helper(self.get_left(node), index, data)
            else:
                update_helper(self.get_right(node), index, data)
            self.set_data(
                node,
                self.merge(
                    self.get_data(self.get_left(node)),
                    self.get_data(self.get_right(node))
                )
            )

        update_helper(self.root, index, data)

    def query(self, start: int, end: int):
        """ Time: O(logN) """
        def query_helper(node, start: int, end: int):
            if node.start == start and node.end == end:
                return self.get_data(node)
            mid = node.start + (node.end - node.start) // 2
            if end <= mid:  # left include mid
                return query_helper(self.get_left(node), start, end)
            if start > mid:
                return query_helper(self.get_right(node), start, end)
            return self.merge(
                query_helper(self.get_left(node), start, mid),
                query_helper(self.get_right(node), mid + 1, end)
            )

        return query_helper(self.root, start, end)


"""
class RedBlackTree(BinaryTree):
    def __init__(self):
        super().__init__()

    def add(self, data):
        pass

    def remove(self, data):
        pass

    def get(self, data):
        pass
"""








































