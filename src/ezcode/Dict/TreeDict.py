from ezcode.Linked.Tree.RedBlackTree import RedBlackTree


class TreeDict:
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

    def __init__(self, init_data=None):
        self.tree = RedBlackTree()
        if init_data is not None:
            for key, value in init_data:
                self[key] = value

    def __contains__(self, key):
        return TreeDict.Entry(key, None) in self.tree

    def __getitem__(self, key):
        node = self.tree.search(TreeDict.Entry(key, None))
        if node is None:
            raise KeyError(f"Key Not Found: {key}")
        return node.data.value

    def __delitem__(self, key):
        self.tree.remove(TreeDict.Entry(key, None))

    def __setitem__(self, key, value):
        node = self.tree.search(TreeDict.Entry(key, None))
        if node is None or node.data.value != value:
            self.tree.remove_node(node)
            self.tree.insert(TreeDict.Entry(key, value))

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
