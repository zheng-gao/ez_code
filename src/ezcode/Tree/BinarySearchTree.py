from typing import Iterable

from ezcode.Tree.BinaryTree import DATA_NAME, LEFT_NAME, RIGHT_NAME
from ezcode.Tree.BinaryTree import BinaryTree, BinaryTreeIterator


class BinarySearchTree(BinaryTree):
    def __init__(self,
        init_data: Iterable = None, root=None, root_copy=None,
        data_name=DATA_NAME, left_name=LEFT_NAME, right_name=RIGHT_NAME
    ):
        super().__init__(
            init_data=init_data, root=root, root_copy=root_copy,
            data_name=data_name, left_name=left_name, right_name=right_name,
            iterator_mode=BinaryTreeIterator.Mode.IN_ORDER, iterator_is_left_first=True
        )

    def __contains__(self, data) -> bool:
        return self.search(data) is not None

    def validate(self) -> bool:
        def _validate(node, left_most, right_most, lower_bound, upper_bound) -> bool:
            if node is None:
                return True
            if node != left_most and not (lower_bound < node.data):
                return False  # node.data should be within boundaries
            if node != right_most and not (node.data < upper_bound):
                return False  # node.data should be within boundaries
            valid_left = _validate(node.left, left_most, right_most, lower_bound, node.data)
            valid_right = _validate(node.right, left_most, right_most, node.data, upper_bound)
            return valid_left and valid_right

        if self.root is None:
            return True
        left_most = self.get_left_most(self.root)
        right_most = self.get_right_most(self.root)
        return _validate(self.root, left_most, right_most, left_most.data, right_most.data)

    def search(self, data, track_parents=False):
        """ O(logN) """
        if track_parents:  # for internal use, e.g. self.remove
            parents, node = [None], self.root  # the None is for the parent of root
            while node is not None:
                if data == node.data:
                    break
                parents.append(node)
                node = node.left if data < node.data else node.right
            return parents, node
        else:
            node = self.root
            while node is not None:
                if data == node.data:
                    break
                node = node.left if data < node.data else node.right
            return node

    def insert(self, data):
        """ O(logN) """
        parents = [None]  # the parent of root is None, track parents for AVLTree and RedBlackTree
        if self.root is None:
            self.root = self.new_node(data=data)
            node = self.root
        else:
            node = self.root
            while node is not None:
                if data == node.data:
                    raise KeyError(f"{data} exist")
                parents.append(node)
                node = node.left if data < node.data else node.right
            parent, node = parents[-1], self.new_node(data=data)
            if data < parent.data:
                parent.left = node
            else:
                parent.right = node
        self.size += 1
        return parents, node

    def remove(self, data):
        """ O(logN) """
        self.remove_node(*self.search(data, track_parents=True))

    def remove_node(self, parents: list, node):
        """
            Time: O(logN)
            parents, removed, successor are made to be compatible with AVLTree/RedBlackTree (no parent pointer)
        """
        replaced, removed = None, None
        if node is not None:
            if node.right is None:
                parent = parents[-1]
                if node == self.root:
                    self.root = node.left
                elif node == parent.left:
                    parent.left = node.left
                else:
                    parent.right = node.left
                replaced, removed = node.left, node
            else:  # left most node of the right tree
                parents.append(node)
                left_most = node.right
                while left_most.left is not None:  # left_most only have the right child
                    parents.append(left_most)
                    left_most = left_most.left
                node.data = left_most.data  # copy data then delete left most
                parent = parents[-1]
                if parent == node:  # never move
                    parent.right = left_most.right  # left_most only have the right child
                else:
                    parent.left = left_most.right
                replaced, removed = left_most.right, left_most
            self.size -= 1
        return replaced, removed

    def remove_range(self, data_lower_bound, data_upper_bound):  # To do: inclusive/exclusive boundary
        if data_upper_bound < data_lower_bound:
            raise ValueError(f"data_upper_bound {data_upper_bound} < data_lower_bound {data_lower_bound}")
        parent, node = None, self.root
        while node is not None:
            if node.data < data_lower_bound:
                parent, node = node, node.right
            elif data_upper_bound < node.data:
                parent, node = node, node.left
            else:
                if node.right is None:
                    if node == self.root:
                        self.root = node.left
                    elif node == parent.left:
                        parent.left = node.left
                    else:
                        parent.right = node.left
                    node = node.left
                else:  # left_most only have the right child
                    left_most_parent, left_most = node, node.right
                    while left_most.left is not None:  # left_most only have the right child
                        left_most_parent, left_most = left_most, left_most.left
                    node.data = left_most.data  # copy data then delete left most
                    if left_most_parent == node:  # never move
                        left_most_parent.right = left_most.right  # left_most only have the right child
                    else:
                        left_most_parent.left = left_most.right
                self.size -= 1

    def pop(self, reverse=False):
        if self.size == 0:
            raise KeyError("Pop from empty tree")
        parents, node = [None], self.root
        if reverse:
            while node.right is not None:
                parents.append(node)
                node = node.right
        else:
            while node.left is not None:
                parents.append(node)
                node = node.left
        saved_data = node.data  # remove_node will swap the data
        self.remove_node(parents, node)
        return saved_data

    def left_rotate(self, parent, node):
        """
        left_rotate & right_rotate keep the tree "Binary Searchable"
        Time: O(1), make node the 'left' child of its right child
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

    def right_rotate(self, parent, node):
        """
        left_rotate & right_rotate keep the tree "Binary Searchable"
        Time: O(1), make node the 'right' child of its left child, keep it BST
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



