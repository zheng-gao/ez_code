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

    def new_node(self, data, left=None, right=None):
        node = self.BinaryTreeNode()
        node.__dict__ = {self.data_name: data, self.left_name: left, self.right_name: right}
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

    def remove_bst_node(self, data):
        # self.root = self.algorithm.remove_bst_node(self.root, data)
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
                else:  # left most node in the right subtree
                    left_most_parent, left_most = node, self.get_right(node)
                    while left_most is not None and self.get_left(left_most) is not None:
                        left_most_parent = left_most
                        left_most = self.get_left(left_most)
                    self.set_data(node, self.get_data(left_most))  # swap data then delete left_most
                    right_child = self.get_right(left_most)  # left_most only have the right child
                    if left_most == self.get_right(node):
                        self.set_right(node, right=right_child)  # left_most_parent == node
                    else:
                        self.set_left(left_most_parent, left=right_child)
                break

    def remove_bst_nodes(self, data_lower_bound, data_upper_bound):
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
                    right_child = self.get_right(left_most)  # left_most only have the right child
                    if left_most == self.get_right(node):
                        self.set_right(node, right=right_child)  # left_most_parent == node
                    else:
                        self.set_left(left_most_parent, left=right_child)


class RandomBinaryTree(BinaryTree):
    def __init__(self, size: int = 0, lower_bound: int = 0, upper_bound: int = 0):
        super().__init__(root=None, data_name="data", left_name="left", right_name="right", algorithm=None)
        self.size = size
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.make_tree()

    def insert(self, data):
        def add_node_helper(node, data):
            if random.randint(0, 1) == 0:
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
            self.insert(random.randint(self.lower_bound, self.upper_bound))


class SegmentTree(BinaryTree):
    """
        SegmentTree is Complete
        Suitable for repeated queries
        Cannot add or delete items once the tree is built
    """
    def __init__(self, merge: Callable = lambda x, y: x + y, data_list: list = None):
        super().__init__(root=None, data_name="data", left_name="left", right_name="right", algorithm=None)
        self.merge = merge  # sum, max, min, gcd or lambda x, y: ...
        if data_list:
            self.build_tree(data_list=data_list)

    def new_node(self, start: int, end: int, data, left=None, right=None):
        node = super().new_node(data, left, right)
        node.__dict__.update({"start": start, "end": end})
        return node

    def node_to_string(self, node):
        return f"[{node.start},{node.end}]:" + str(node.data)

    def build_tree(self, data_list: list):
        """ Time: O(N), Space: O(N) """
        def build_tree_helper(start: int, end: int):
            if start == end:
                return self.new_node(start=start, end=end, data=data_list[start])
            mid = start + (end - start) // 2
            left, right = build_tree_helper(start, mid), build_tree_helper(mid + 1, end)  # left include mid
            return self.new_node(start, end, self.merge(left.data, right.data), left, right)

        self.root = build_tree_helper(0, len(data_list) - 1)

    def update(self, index: int, data):
        """ Time: O(logN) """
        def update_helper(node, index: int, data):
            if node.start == node.end == index:
                node.data = data
                return
            mid = node.start + (node.end - node.start) // 2
            if index <= mid:  # left include mid
                update_helper(node.left, index, data)
            else:
                update_helper(node.right, index, data)
            node.data = self.merge(node.left.data, node.right.data)

        update_helper(self.root, index, data)

    def query(self, start: int, end: int):
        """ Time: O(logN) """
        def query_helper(node, start: int, end: int):
            if node.start == start and node.end == end:
                return node.data
            mid = node.start + (node.end - node.start) // 2
            if end <= mid:  # left include mid
                return query_helper(node.left, start, end)
            if start > mid:
                return query_helper(node.right, start, end)
            return self.merge(
                query_helper(node.left, start, mid),
                query_helper(node.right, mid + 1, end)
            )

        return query_helper(self.root, start, end)


class RedBlackTree(BinaryTree):
    def __init__(self):
        super().__init__(root=None, data_name="data", left_name="left", right_name="right", algorithm=None)

    def new_node(self, data, is_red=True, parent=None, left=None, right=None):
        node = super().new_node(data, left, right)
        node.__dict__.update({"is_red": is_red, "parent": parent})
        return node

    def _rotate(self, node, is_left_rotation=True):
        parent = node.parent
        if is_left_rotation:
            """
            left rotate: O(1)
            make node the 'left' child of its right child, keep it BST
                            <------------
                  (P)─┐┌─(P)              (P)─┐┌─(P)
                  ┌───(R)───┐           ┌───(node)───┐
             ┌──(node)──┐  (x)         (x)       ┌──(R)──┐
            (x)        (RL)                     (RL)    (x)
            """
            right, right_left = node.right, node.right.left
            node.right = right_left
            if right_left is not None:
                right_left.parent = node
            right.left, node.parent, right.parent = node, right, parent
            if parent is None:
                self.root = right  # might change the color of root
            elif parent.left == node:
                parent.left = right
            else:
                parent.right = right
        else:
            """
            right rotate: O(1)
            make node the 'right' child of its left child, keep it BST
                             ------------>
                   (P)─┐┌─(P)              (P)─┐┌─(P)
                 ┌───(node)───┐            ┌───(L)───┐
             ┌──(L)──┐       (x)          (x)   ┌──(node)──┐
            (x)     (LR)                       (LR)       (x)
            """
            left, left_right = node.left, node.left.right
            node.left = left_right
            if left_right is not None:
                left_right.parent = node
            left.right, node.parent, left.parent = node, left, parent
            if parent is None:
                self.root = left  # might change the color of root
            elif parent.left == node:
                parent.left = left
            else:
                parent.right = left
        self.root.is_red = False  # root is black

    def insert(self, data):
        """ O(logN) """
        if self.root is None:
            self.root = self.new_node(data=data, is_red=False)  # root is black
            return
        parent, node = None, self.root
        while node is not None:
            if data == node.data:
                raise KeyError(f"{data} exist")
            parent, node = node, node.left if data < node.data else node.right
        node = self.new_node(data=data, is_red=True, parent=parent)
        if data < parent.data:
            parent.left = node
        else:
            parent.right = node
        # Insert Fix Up
        while parent is not None and parent.is_red:  # black parent won't violate the RB tree constraints
            grand = parent.parent  # grand parent exists and it is black
            uncle = grand.right if parent == grand.left else grand.left
            if uncle.is_red:  # paint(parent:black, uncle:black, grand:red)
                parent.is_red, uncle.is_red, grand.is_red = False, False, True
                node, parent = grand, grand.parent
            else:  # uncle is black
                if parent == grand.left:
                    if node == parent.right:
                        self._rotate(parent, is_left_rotation=True)
                        """
                              ┌───────(G.b)───────┐       -->            ┌─────(G.b)─────┐
                         ┌──(P.r)──┐         ┌──(U.b)──┐            ┌──(N.r)──┐     ┌──(U.b)──┐
                        (x)   ┌──(N.r)──┐   (x)       (x)      ┌──(P.r)──┐   (x)   (x)       (x)
                             (C)       (x)                    (x)       (C)
                        """
                        parent, node = node, parent  # node becomes parent.left
                    self._rotate(grand, is_left_rotation=False)
                    """
                               ┌─────(G.b)─────┐       -->       ┌─────(P.r)─────┐
                          ┌──(P.r)──┐     ┌──(U.b)──┐       ┌──(N.r)──┐     ┌──(G.b)──┐
                     ┌──(N.r)──┐   (C)   (x)       (x)     (x)       (x)   (C)   ┌──(U.b)──┐
                    (x)       (x)                                               (x)       (x)
                    """
                    if grand == self.root:
                        self.root = parent
                    parent.is_red, grand.is_red = False, True  # paint(parent:black, grand:red), exit while loop
                    """
                          ┌─────(P.b)─────┐
                     ┌──(N.r)──┐     ┌──(G.r)──┐
                    (x)       (x)   (C)   ┌──(U.b)──┐
                                         (x)       (x)
                    """
                else:  # parent == grand.right
                    if node == parent.left:
                        self._rotate(parent, is_left_rotation=False)
                        parent, node = node, parent
                    self.left_rotate(grand, is_left_rotation=True)
                    if grand == self.root:
                        self.root = parent
                    parent.is_red, grand.is_red = False, True  # paint(parent:black, grand:red), exit while loop
        self.root.is_red = False  # red uncle process might change the color of root

    def find_node(self, data):
        node = self.root
        while node is not None:
            if data == node.data:
                break
            node = node.left if data < node.data else node.right
        return node

    def find_left_most_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def remove(self, data):
        node = self.find_node(data)
        if node is None:
            return
        if node.right is None:
            if node == self.root:
                self.root = node.left
                if node.left is not None:
                    node.left.parent = None
            elif node == node.parent.left:
                node.parent.left = node.left
                if node.left is not None:
                    node.left.parent = node.parent
            else:
                node.parent.right = node.left
                if node.left is not None:
                    node.left.parent = node.parent
            if not node.is_red:  # deleted a black node
                if node.left is None or not node.left.is_red:  # double black
                    pass  # Delete Fix Up
                else:
                    node.left.is_red = False
        else:
            left_most = self.find_left_most_node(node.right)  # left_most only have the right child
            left_most.data, node.data = node.data, left_most.data  # swap data then delete left most, color untouched
            if left_most == node.right:
                node.right = left_most.right
                if left_most.right is not None:
                    left_most.right.parent = node
            else:
                left_most.parent.left = left_most.right
                if left_most.right is not None:
                    left_most.right.parent = left_most.parent
            if not left_most.is_red:  # deleted a black node
                if left_most.right is None or not left_most.right.is_red:  # double black
                    pass  # Delete Fix Up
                else:
                    left_most.right.is_red = False

    def remove_fix_up(self):
        pass


















































