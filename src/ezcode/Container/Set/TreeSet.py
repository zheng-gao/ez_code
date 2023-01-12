from typing import Iterable

from ezcode.Container.Tree.RedBlackTree import RedBlackTree


class TreeSet:
    def __init__(self, init_data: Iterable = None):
        self.tree = RedBlackTree()
        if init_data is not None:
            for key in init_data:
                self.tree.insert(key)

    def __contains__(self, key):
        return key in self.tree

    def __iter__(self):
        return iter(self.tree)

    def __reversed__(self):
        return reversed(self.tree)

    def __repr__(self):
        return repr(list(iter(self)))

    def add(self, key):
        if key not in self:
            self.tree.insert(key)

    def remove(self, key):
        self.tree.remove(key)

    def pop(self):
        return self.tree.pop()

    def update(self, other: Iterable):
        for key in other:
            self.add(key)

    def clear(self):
        self.tree.clear()
