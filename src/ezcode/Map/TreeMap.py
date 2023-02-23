from collections.abc import Mapping, MutableMapping
from enum import Enum

from ezcode.Tree.BinaryTreeIterator import BinaryTreeIterator
from ezcode.Tree.RedBlackTree import RedBlackTree
from ezcode.Tree.BinarySearchTree import BinarySearchTree


class TreeMapIterator:
    Mode = Enum("Mode", ["KEY", "VALUE", "ITEM"])

    def __init__(self, tree, reverse=False, mode=Mode.KEY):
        self.mode = mode
        self.iterator = BinaryTreeIterator(
            node=tree.root,
            mode=BinaryTreeIterator.Mode.IN_ORDER,
            is_left_first=(not reverse),
            data_name=tree.data_name,
            left_name=tree.left_name,
            right_name=tree.right_name
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self.mode == TreeMapIterator.Mode.KEY:
            return next(self.iterator).key
        elif self.mode == TreeMapIterator.Mode.VALUE:
            return next(self.iterator).value
        else:
            entry = next(self.iterator)
            return entry.key, entry.value


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
        return TreeMapIterator(tree=self.tree, reverse=False, mode=TreeMapIterator.Mode.KEY)

    def __reversed__(self):
        return TreeMapIterator(tree=self.tree, reverse=True, mode=TreeMapIterator.Mode.KEY)

    def __str__(self):
        return "{" + ", ".join([f"{key}: {value}" for key, value in self.items()]) + "}"

    def clear(self):
        self.tree.clear()

    def keys(self, reverse=False):
        yield from TreeMapIterator(tree=self.tree, reverse=reverse, mode=TreeMapIterator.Mode.KEY)

    def values(self, reverse=False):
        yield from TreeMapIterator(tree=self.tree, reverse=reverse, mode=TreeMapIterator.Mode.VALUE)

    def items(self, reverse=False):
        yield from TreeMapIterator(tree=self.tree, reverse=reverse, mode=TreeMapIterator.Mode.ITEM)

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

    def update(self, other):
        if not isinstance(other, Mapping):
            raise TypeError
        for key, value in other.items():
            self[key] = value


