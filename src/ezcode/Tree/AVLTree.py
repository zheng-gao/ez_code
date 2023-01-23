from __future__ import annotations

from typing import Iterable

from ezcode.Tree.BinarySearchTree import BinarySearchTree


class AVLTree(BinarySearchTree):
    def __init__(self, init_data: Iterable = None, root=None, root_copy=None):
        super().__init__(
            init_data=init_data, root=root, root_copy=root_copy,
            data_name="data", left_name="left", right_name="right"
        )

    def new_node(self, height: int = 1, data=None, left=None, right=None):
        node = super().new_node(data=data, left=left, right=right)
        node.__dict__["height"] = height
        return node

    def node_to_string(self, node) -> str:
        return f"{node.data}|H:{node.height}|B:{self._get_balance_factor(node)}"

    def _update_height(self, node):
        if node is not None:
            height = node.height
            if node.left is None and node.right is None:
                node.height = 1
            elif node.left is not None and node.right is not None:
                node.height = max(node.left.height, node.right.height) + 1
            else:
                node.height = (node.right.height + 1) if node.left is None else (node.left.height + 1)
            return False if height == node.height else True
        return False

    def _get_balance_factor(self, node) -> int:
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 0
        if node.left is not None and node.right is not None:
            return node.left.height - node.right.height
        return node.right.height if node.left is None else node.left.height

    def _left_rotate(self, parent, node):
        """
        Time: O(1)
        make node the 'left' child of its right child, keep it BST
                         <----------
              (P)─┐┌─(P)              (P)─┐┌─(P)
              ┌───(R)───┐           ┌───(node)───┐
         ┌──(node)──┐  (x)         (x)       ┌──(R)──┐
        (x)        (RL)                     (RL)    (x)
        """
        right = node.right
        node.right, right.left = right.left, node
        if parent is None:
            self.root = right
        elif parent.left == node:
            parent.left = right
        else:
            parent.right = right

    def _right_rotate(self, parent, node):
        """
        Time: O(1)
        make node the 'right' child of its left child, keep it BST
                           ---------->
               (P)─┐┌─(P)              (P)─┐┌─(P)
             ┌───(node)───┐            ┌───(L)───┐
         ┌──(L)──┐       (x)          (x)   ┌──(node)──┐
        (x)     (LR)                       (LR)       (x)
        """
        left = node.left
        node.left, left.right = left.right, node
        if parent is None:
            self.root = left
        elif parent.left == node:
            parent.left = left
        else:
            parent.right = left

    def insert(self, data):
        """ Time: O(logN) """
        if self.root is None:
            self.root = self.new_node(data=data, height=1)
        else:
            parents, node = list(), self.root
            while node is not None:
                if data == node.data:
                    raise KeyError(f"{data} exist")
                parents.append(node)
                node = node.left if data < node.data else node.right
            node = self.new_node(data=data, height=1)
            parent = parents.pop()
            if data < parent.data:
                parent.left = node
            else:
                parent.right = node
            grand_parent = parents.pop() if len(parents) > 0 else None
            if parent.left is None or parent.right is None:  # else: parent has two children, no further processing is required
                is_height_updated = self._update_height(parent)
                while is_height_updated and grand_parent is not None and abs(self._get_balance_factor(grand_parent)) != 2:
                    node, parent, grand_parent = parent, grand_parent, parents.pop() if len(parents) > 0 else None  # search up
                    is_height_updated = self._update_height(parent)
                if is_height_updated and grand_parent is not None:  # else: not found unbalanced subtree, no further processing is required
                    greate_grand_parent = parents.pop() if len(parents) > 0 else None
                    if parent == grand_parent.left:
                        if node == parent.left:  # Case LL
                            self._right_rotate(parent=greate_grand_parent, node=grand_parent)
                        else:  # Case LR
                            self._left_rotate(parent=grand_parent, node=parent)
                            parent.height -= 1
                            node.height += 1
                            self._right_rotate(parent=greate_grand_parent, node=grand_parent)
                    else:
                        if node == parent.right:  # Case RR
                            self._left_rotate(parent=greate_grand_parent, node=grand_parent)
                        else:  # Case RL
                            self._right_rotate(parent=grand_parent, node=parent)
                            parent.height -= 1
                            node.height += 1
                            self._left_rotate(parent=greate_grand_parent, node=grand_parent)
                    grand_parent.height -= 1
        self.size += 1

    def remove(self, data):
        """ O(logN) """
        parents, node = self.search(data, track_parents=True)
        self.remove_node(parents=parents, node=node)

#    def remove_node(self, parents, node):
#        """ O(logN) """
#        if node is not None:
#            parent = parents.pop() if len(parents) > 0 else None
#            if node.right is None:
#                if node == self.root:
#                    self.root = node.left
#                else:
#                    if node == parent.left:
#                        parent.left = node.left
#                    else:
#                        parent.right = node.left
#                    # ...
#            else:
#                left_most = node.right             # left most node of the right tree
#                while left_most.left is not None:  # left_most only have the right child
#                    left_most = left_most.left
#                left_most.data, node.data = node.data, left_most.data  # swap data then delete left most
#                if left_most == node.right:
#                    node.right = left_most.right
#                else:
#                    left_most.parent.left = left_most.right
#                    if left_most.right is not None:
#                        left_most.right.parent = left_most.parent
#                if not left_most.is_red:                                       # deleted a black node
#                    if left_most.right is None or not left_most.right.is_red:  # missing a black node
#                        self._remove_fix_up(parent=left_most.parent, node=left_most.right)
#                    else:
#                        left_most.right.is_red = False
#            self.size -= 1
#
#
#
#
#     def __eq__(self, other: AVLTree) -> bool:
#         def _tree_equal(node_1, node_2):
#             if node_1 is None and node_2 is None:
#                 return True
#             if node_1 is None or node_2 is None:
#                 return False
#             if node_1.data != node_2.data or node_1.is_red != node_2.is_red:
#                 return False
#             return _tree_equal(node_1.left, node_2.left) and _tree_equal(node_1.right, node_2.right)
#
#         return _tree_equal(self.root, other.root)
#
#     def copy_tree(self, node):
#         if node is None:
#             return None, 0
#         if not (self.root is None and self.new_node().match(node)) and not self.root.match(node):
#             raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
#         root_copy, size_copy = self.copy_node(node), 0
#         queue, queue_copy = deque([node]), deque([root_copy])
#         while len(queue) > 0:
#             node = queue.popleft()
#             node_copy = queue_copy.popleft()
#             size_copy += 1
#             if node.left is not None:
#                 node_copy.left = self.copy_node(node.left)
#                 node_copy.left.parent = node_copy
#                 queue.append(node.left)
#                 queue_copy.append(node_copy.left)
#             if node.right is not None:
#                 node_copy.right = self.copy_node(node.right)
#                 node_copy.right.parent = node_copy
#                 queue.append(node.right)
#                 queue_copy.append(node_copy.right)
#         return root_copy, size_copy
#
#     def copy(self) -> RedBlackTree:
#         tree = RedBlackTree()
#         tree.root, tree.size = self.copy_tree(self.root)
#         return tree
#
#    def validate(self) -> bool:
#        """
#        Binary Searchable.
#        Root is always black.
#        All NULL leaves are black, and both children of a red node are black.
#        Every simple path from a given node to any of its descendant leaves contains the same number of black nodes.
#        Path from root to farthest leaf is no more than twice as long as the path from the root to nearest leaf.
#        """
#        def _validate(node) -> tuple[bool, int, int, int]:  # is_rb_tree, max_path_length, min_path_length, black_node_count
#            if node is None:
#                return True, 0, 0, 0
#            if node.is_red and ((node.left is not None and node.left.is_red) or (node.right is not None and node.right.is_red)):
#                return False, 0, 0, 0
#            left_is_rb_tree, left_max_path_length, left_min_path_length, left_black_node_count = _validate(node.left)
#            if not left_is_rb_tree or (left_min_path_length << 1) < left_max_path_length:
#                return False, 0, 0, 0
#            right_is_rb_tree, right_max_path_length, right_min_path_length, right_black_node_count = _validate(node.right)
#            if not right_is_rb_tree or (right_min_path_length << 1) < right_max_path_length:
#                return False, 0, 0, 0
#            if left_black_node_count != right_black_node_count:
#                return False, 0, 0, 0
#            max_path_length = max(left_max_path_length, right_max_path_length) + 1
#            min_path_length = min(left_min_path_length, right_min_path_length) + 1
#            black_node_count = left_black_node_count + (0 if node.is_red else 1)
#            return True, max_path_length, min_path_length, black_node_count
#
#        if self.root is None:
#            return True
#        if self.root.is_red:
#            return False
#        if super().validate():  # Binary Searchable
#            return _validate(self.root)[0]
#        return False





