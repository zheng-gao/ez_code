from __future__ import annotations

from collections import deque
from enum import Enum
from math import ceil
from sys import maxsize
from typing import Callable

# Tree Node
DATA_NAME = "data"
LEFT_NAME = "left"
RIGHT_NAME = "right"
# Printer
LEFT_WING = "─"
RIGHT_WING = "─"
LEFT_WING_HEAD = "┌"
RIGHT_WING_HEAD = "┐"
LEFT_WING_TAIL = "("
RIGHT_WING_TAIL = ")"


class BinaryTreeIterator:
    Mode = Enum("Mode", ["DFS", "BFS", "PRE_ORDER", "IN_ORDER", "POST_ORDER"])

    def __init__(self, node=None, mode: Mode = Mode.DFS, is_left_first: bool = True,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME
    ):
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.child_selector = self._left_first if is_left_first else self._right_first
        if mode == BinaryTreeIterator.Mode.DFS or mode == BinaryTreeIterator.Mode.PRE_ORDER:
            self.generator = self._pre_order(node)
        elif mode == BinaryTreeIterator.Mode.IN_ORDER:
            self.generator = self._in_order(node)
        elif mode == BinaryTreeIterator.Mode.POST_ORDER:
            self.generator = self._post_order(node)
        else:  # BFS
            self.generator = self._bfs(node)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generator).__dict__[self.data_name]

    def _left_first(self, node):
        if node is not None:
            yield node.__dict__[self.left_name]
            yield node.__dict__[self.right_name]

    def _right_first(self, node):
        if node is not None:
            yield node.__dict__[self.right_name]
            yield node.__dict__[self.left_name]

    def _pre_order(self, node):
        if node is not None:
            yield node
            for child in self.child_selector(node):
                yield from self._pre_order(child)

    def _in_order(self, node):
        if node is not None:
            can_yield = True
            for child in self.child_selector(node):
                yield from self._in_order(child)
                if can_yield:
                    yield node
                can_yield = False

    def _post_order(self, node):
        if node is not None:
            for child in self.child_selector(node):
                yield from self._post_order(child)
            yield node

    # def _bfs(self, node, depth):
    #     if node is not None and depth < self.height:
    #         yield node
    #         for child in self._bfs(node, depth + 1):
    #             yield from self.child_selector(child)
    def _bfs(self, node):
        if node is not None:
            queue = deque([node])
            while len(queue) > 0:
                node = queue.popleft()
                yield node
                for child in self.child_selector(node):
                    if child is not None:
                        queue.append(child)


class BinaryTree(object):

    class BinaryTreeNode(object):
        def __init__(self):
            pass

    def __init__(self, root=None,
        data_name: str = DATA_NAME,
        left_name: str = LEFT_NAME,
        right_name: str = RIGHT_NAME,
        iterator_mode: BinaryTreeIterator.Mode = BinaryTreeIterator.Mode.DFS,
        iterator_is_left_first: bool = True,
        algorithm: BinaryTreeAlgorithm = None
    ):
        self.root = root
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.iterator_mode = iterator_mode
        self.iterator_is_left_first = iterator_is_left_first
        self.algorithm = algorithm if algorithm is not None else BinaryTreeAlgorithm(data_name, left_name, right_name)

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
        return any(d == data for d in iter(self))

    def __str__(self) -> str:
        return self.to_string()

    def new_node(self, data, left=None, right=None):
        node = self.BinaryTreeNode()
        node.__dict__ = {self.data_name: data, self.left_name: left, self.right_name: right}
        return node

    def node_to_string(self, node) -> str:
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
        pass

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
        return self.is_copied(root_1.__dict__[self.left_name], root_2.__dict__[self.left_name]) and self.is_copied(root_1.__dict__[self.right_name], root_2.__dict__[self.right_name])

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


class BinaryTreePrinter:
    class IndexedNode:
        def __init__(self, index, node):
            self.index = index
            self.node = node

    def __init__(self,
        data_name: str = DATA_NAME,
        left_name: str = LEFT_NAME,
        right_name: str = RIGHT_NAME,
        left_wing: str = LEFT_WING,
        left_wing_head: str = LEFT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL,
        right_wing: str = RIGHT_WING,
        right_wing_head: str = RIGHT_WING_HEAD,
        right_wing_tail: str = RIGHT_WING_TAIL,
        node_to_string: Callable = None
    ):
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.left_wing = left_wing
        self.left_wing_head = left_wing_head
        self.left_wing_tail = left_wing_tail
        self.right_wing = right_wing
        self.right_wing_head = right_wing_head
        self.right_wing_tail = right_wing_tail
        self.tree_depth = 0
        self.max_data_string_length = 0
        self.char_map = list()
        self.node_to_string = node_to_string if node_to_string is not None else lambda node: str(node.__dict__[self.data_name])

    def get_left(self, node):
        return node.__dict__[self.left_name]

    def get_right(self, node):
        return node.__dict__[self.right_name]

    def _align_to_center(self, node, is_last_line):
        """ e.g.
        max data string length: 10
        data length: 3
        pre padding length: 4
        post padding length: 3
        pre padding char: -
        post padding char: -
        left wing tail: <
        right wing tail: >
        ---<ABC>--
        """
        pre_padding_length = ceil((self.max_data_string_length - len(self.node_to_string(node))) / 2)  # even length padding more, use larger mid index
        post_padding_length = self.max_data_string_length - len(self.node_to_string(node)) - pre_padding_length
        pre_padding_char = " " * len(self.left_wing) if is_last_line or self.get_left(node) is None else self.left_wing
        post_padding_char = " " * len(self.right_wing) if is_last_line or self.get_right(node) is None else self.right_wing
        pre_padding_string = f"{pre_padding_char * (pre_padding_length - 1)}{self.left_wing_tail}"
        post_padding_string = f"{self.right_wing_tail}{post_padding_char * (post_padding_length - 1)}"
        return f"{pre_padding_string}{self.node_to_string(node)}{post_padding_string}"

    def _set_data_string(self, line_to_print, indexed_node, depth):

        def _get_mid_index(depth, index, line_length):
            slot_count = pow(2, depth)
            slot_id = index * 2 - slot_count + 1
            return int(line_length * slot_id / slot_count)

        data_string = self._align_to_center(indexed_node.node, depth == self.tree_depth)
        start_index = _get_mid_index(depth, indexed_node.index, len(line_to_print)) - int(self.max_data_string_length / 2)
        line_to_print[start_index:(start_index + self.max_data_string_length)] = list(data_string)
        if depth != self.tree_depth:
            if self.get_left(indexed_node.node) is not None:
                left_child_mid_index = _get_mid_index(depth + 1, indexed_node.index * 2, len(line_to_print))
                line_to_print[(left_child_mid_index + 1):start_index] = list(self.left_wing * (start_index - left_child_mid_index - 1))
                line_to_print[left_child_mid_index] = self.left_wing_head
            if self.get_right(indexed_node.node) is not None:
                right_child_mid_index = _get_mid_index(depth + 1, indexed_node.index * 2 + 1, len(line_to_print))
                line_to_print[(start_index + self.max_data_string_length):right_child_mid_index] = list(self.right_wing * (right_child_mid_index - start_index - self.max_data_string_length))
                line_to_print[right_child_mid_index] = self.right_wing_head

    def _collect_tree_info(self, node):
        """ return depth and update max_data_string_length """
        if node is None:
            return 0
        data_str_len = len(self.node_to_string(node)) + len(self.left_wing_head) + len(self.right_wing_head) + len(self.left_wing_tail) + len(self.right_wing_tail)
        self.max_data_string_length = max(data_str_len, self.max_data_string_length)
        left_depth = self._collect_tree_info(self.get_left(node)) if self.get_left(node) is not None else 0
        right_depth = self._collect_tree_info(self.get_right(node)) if self.get_right(node) is not None else 0
        return max(left_depth, right_depth) + 1

    def _make_char_map(self, node):
        self.char_map, self.max_data_string_length = list(), 0
        self.tree_depth = self._collect_tree_info(node)
        last_line_data_count = pow(2, self.tree_depth - 1)
        last_line_string_length = last_line_data_count * (self.max_data_string_length + 1) - 1  # +one space in between
        """
        [PrePadding][LeftWingTail][Data][RightWingTail][PostPadding][SPACE][PrePadding][LeftWingTail][Data][RightWingTail][PostPadding][SPACE]...
        """
        queue = deque()
        queue.append(BinaryTreePrinter.IndexedNode(1, node))
        children_found, children_left, depth = 0, 1, 1
        line_to_print = list(" " * last_line_string_length)  # we have to make it a list because string is immutable
        while len(queue) > 0:
            indexed_node = queue.popleft()
            children_left -= 1
            self._set_data_string(line_to_print, indexed_node, depth)
            if self.get_left(indexed_node.node) is not None:
                queue.append(BinaryTreePrinter.IndexedNode(int(indexed_node.index * 2), self.get_left(indexed_node.node)))
                children_found += 1
            if self.get_right(indexed_node.node) is not None:
                queue.append(BinaryTreePrinter.IndexedNode(int(indexed_node.index * 2) + 1, self.get_right(indexed_node.node)))
                children_found += 1
            if children_left == 0:
                self.char_map.append(line_to_print)
                children_left = children_found
                children_found = 0
                line_to_print = list(" " * last_line_string_length)
                depth += 1

    def to_string(self, node, trim_left=True, trim_right=True):
        if node is None:
            return "None\n"
        self._make_char_map(node)
        start_print_index, end_print_index = 0, len(self.char_map[0])
        if trim_left:  # trim left blank
            for line in self.char_map:
                last_non_blank_index_from_start = 0
                for char in line:
                    if char == " ":
                        last_non_blank_index_from_start += 1
                    else:
                        break
                if start_print_index == 0 or last_non_blank_index_from_start < start_print_index:
                    start_print_index = last_non_blank_index_from_start
        if trim_right:  # trim right blank
            for line in self.char_map:
                last_non_blank_index_from_end = len(self.char_map[0])
                for char in line[::-1]:
                    if char == " ":
                        last_non_blank_index_from_end -= 1
                    else:
                        break
                if end_print_index == len(self.char_map[0]) or last_non_blank_index_from_end > end_print_index:
                    end_print_index = last_non_blank_index_from_end
        output_string = ""
        for line in self.char_map:
            output_string += "".join(line[start_print_index:end_print_index]) + "\n"
        return output_string

    def print(self, node, trim_left=True, trim_right=True):
        print("\n" + self.to_string(node, trim_left, trim_right))
