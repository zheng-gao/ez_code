
class Trie:
    class Node:
        def __init__(self, data=None, count=1):
            self.data = data
            self.count = count
            self.is_end = False
            self.children = None  # {data: Node}

    def __init__(self):
        self.root = self.Node(data="^", count=0)

    def clear(self):
        if self.root.count > 0:
            self.root = self.Node(data="^", count=0)

    def get_child(self, node, data):
        if not node.children or data not in node.children:
            return None
        return node.children[data]

    def size(self):
        return self.root.count

    def __str__(self):

        def _to_string_pre_order(node, str_list, result):
            if node:
                if node.is_end:
                    str_list.append(f"{node.data}:{node.count}:$")
                else:
                    str_list.append(f"{node.data}:{node.count}")
                if not node.children:
                    result.append(" -> ".join(str_list))
                else:
                    for child_node in node.children.values():
                        _to_string_pre_order(child_node, str_list, result)
                str_list.pop()

        result = list()
        _to_string_pre_order(self.root, list(), result)
        return "\n".join(result) + "\n"

    def print(self):
        print(self, end="")

    def add(self, prefix: list):
        if prefix is None:
            raise ValueError("prefix cannot be None")
        node = self.root
        node.count += 1
        for data in prefix:
            next_node = self.get_child(node, data)
            if next_node:
                node = next_node
                node.count += 1
            else:
                new_node = self.Node(data=data, count=1)
                if not node.children:
                    node.children = dict()
                node.children[data] = new_node
                node = new_node
        node.is_end = True

    def contains(self, prefix: list, strict=False):
        if prefix is None:
            raise ValueError("prefix cannot be None")
        node = self.root
        for data in prefix:
            node = self.get_child(node, data)
            if not node:
                return False
        if strict:
            return node.is_end
        return True

    def longest_common_prefix(self):
        node, prefix = self.root, list()
        while node:
            next_node = None
            if node.children:
                for child_node in node.children.values():
                    if child_node and child_node.count == self.root.count:
                        prefix.append(child_node.data)
                        next_node = child_node
                        break
            node = next_node
        return prefix

    def prefix_wildcard(self, prefix: list = None):

        def _prefix_wildcard_pre_order(node, data_list, result):
            if node:
                if node != self.root:
                    data_list.append(node.data)
                if node.is_end:
                    result.append(data_list.copy())
                if node.children:
                    for child_node in node.children.values():
                        _prefix_wildcard_pre_order(child_node, data_list, result)
                if len(data_list) > 0:
                    data_list.pop()

        result = list()
        if not prefix:
            _prefix_wildcard_pre_order(self.root, list(), result)
        else:
            node = self.root
            for data in prefix:
                node = self.get_child(node, data)
                if not node:
                    return None
            _prefix_wildcard_pre_order(node, list(prefix)[:-1:].copy(), result)
        return result


class SuffixTrie(Trie):
    def __init__(self, data_list: list = None):
        super().__init__()
        self.build(data_list)

    def build(self, data_list: list):
        self.clear()
        for i in range(len(data_list)):
            self.add(data_list[i:])

