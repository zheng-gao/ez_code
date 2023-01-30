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
        """ remove raise KeyError if key not found """
        parents, node = self.tree.search(data=key, track_parents=True)
        if node is None:
            raise KeyError(f"Not Found: {key}")
        self.tree.remove_node(parents, node)

    def discard(self, key):
        """ discard not raise error if key not found """
        self.tree.remove(key)

    def pop(self, reverse=False):
        if len(self.tree) == 0:
            raise KeyError("Pop from empty set")
        return self.tree.pop(reverse=reverse)

    def update(self, other: Iterable):
        for key in other:
            self.add(key)

    def clear(self):
        self.tree.clear()
