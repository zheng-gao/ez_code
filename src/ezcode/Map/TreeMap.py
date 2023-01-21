from typing import Iterable

from ezcode.Tree.RedBlackTree import RedBlackTree


class TreeMap:
    class Entry:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value

        def __lt__(self, other):
            return self.key < other.key

        def __gt__(self, other):
            return self.key > other.key

        def __eq__(self, other):
            return self.key == other.key

        def __str__(self):
            return f"{repr(self.key)},{repr(self.value)}"  # for tree printer

        def __repr__(self):
            return f"({repr(self.key)}, {repr(self.value)})"

    def __init__(self, init_data: Iterable = None):
        self.tree = RedBlackTree()
        if init_data is not None:
            for key, value in init_data:
                self[key] = value

    def __len__(self):
        return len(self.tree)

    def __contains__(self, key):
        return TreeMap.Entry(key, None) in self.tree

    def __getitem__(self, key):
        node = self.tree.search(TreeMap.Entry(key, None))
        if node is None:
            raise KeyError(f"Key Not Found: {key}")
        return node.data.value

    def __delitem__(self, key):
        self.tree.remove(TreeMap.Entry(key, None))

    def __setitem__(self, key, value):
        parent, node = self.tree.search(TreeMap.Entry(key, None), return_with_parent=True)
        if node is None or node.data.value != value:
            self.tree.remove_node(parent, node)
            self.tree.insert(TreeMap.Entry(key, value))

    def __iter__(self):
        return iter(self.tree)  # node.data -> entry(key, value)

    def __reversed__(self):
        return reversed(self.tree)

    def __repr__(self):
        return repr(list(iter(self)))

    def keys(self, reverse=False):
        if reverse:
            for entry in reversed(self):
                yield entry.key
        else:
            for entry in self:
                yield entry.key

    def values(self, reverse=False):
        if reverse:
            for entry in reversed(self):
                yield entry.value
        else:
            for entry in self:
                yield entry.value

    def items(self, reverse=False):
        if reverse:
            for entry in reversed(self):
                yield entry.key, entry.value
        else:
            for entry in self:
                yield entry.key, entry.value

    def clear(self):
        self.tree.clear()

    def pop(self, key):
        parent, node = self.tree.search(TreeMap.Entry(key, None), return_with_parent=True)
        if node is None:
            raise KeyError(f"Key Not Found: {key}")
        saved_value = node.data.value        # save this value before remove_node
        self.tree.remove_node(parent, node)  # will swap node.data
        return saved_value

    def popitem(self, reverse=False):
        return self.tree.pop(reverse=reverse)

