from collections.abc import MutableSet
from typing import Iterable

from ezcode.Tree.RedBlackTree import RedBlackTree
from ezcode.Tree.BinarySearchTree import BinarySearchTree


class TreeSet(MutableSet):
    def __init__(self, init_data: Iterable = None, tree: BinarySearchTree = RedBlackTree()):
        self.tree = tree
        if init_data is not None:
            for key in init_data:
                self.tree.insert(key)

    def __len__(self):
        return len(self.tree)

    def __contains__(self, key):
        return key in self.tree

    def __iter__(self):
        return iter(self.tree)

    def __reversed__(self):
        return reversed(self.tree)

    def __repr__(self):
        return repr(list(iter(self)))

    def add(self, key):
        parents, node = self.tree.search(data=key, track_parents=True)
        if node is None:
            self.tree.insert_node(parents, self.tree.new_node(data=key))

    def remove(self, key):
        self.tree.remove(key)

    def discard(self, key):
        """ Same as remove, required by collections.abc.MutableSet """
        self.tree.remove(key)

    def pop(self, reverse=False):
        return self.tree.pop(reverse=reverse)

    def update(self, other: Iterable):
        for key in other:
            self.add(key)

    def clear(self):
        self.tree.clear()
