from collections.abc import MutableMapping

from ezcode.Tree.RedBlackTree import RedBlackTree
from ezcode.Tree.BinarySearchTree import BinarySearchTree


class TreeMap(MutableMapping):
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

    def __init__(self, init_map=None, tree: BinarySearchTree = RedBlackTree()):
        self.tree = tree
        if init_map is not None:
            for key, value in init_map.items():
                self[key] = value

    def __len__(self):
        return len(self.tree)

    def __contains__(self, key):
        return TreeMap.Entry(key, None) in self.tree

    def __getitem__(self, key):
        node = self.tree.search(data=TreeMap.Entry(key, None), track_parents=False)
        if node is None:
            raise KeyError(f"Not Found: {key}")
        return node.data.value

    def __delitem__(self, key):
        parents, node = self.tree.search(data=TreeMap.Entry(key, None), track_parents=True)
        if node is None:
            raise KeyError(f"Not Found: {key}")
        self.tree.remove_node(parents, node)

    def __setitem__(self, key, value):
        data = TreeMap.Entry(key, value)
        parents, node = self.tree.search(data=data, track_parents=True)
        if node is None:
            self.tree.insert_node(parents, self.tree.new_node(data=data))
        else:
            node.data.value = value

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
        parents, node = self.tree.search(data=TreeMap.Entry(key, None), track_parents=True)
        if node is None:
            raise KeyError(f"Not Found: {key}")
        saved_value = node.data.value         # save this value before remove_node
        self.tree.remove_node(parents, node)  # will swap node.data
        return saved_value

    def popitem(self, reverse=False):
        if len(self.tree) == 0:
            raise KeyError("Pop from empty map")
        return self.tree.pop(reverse=reverse)

