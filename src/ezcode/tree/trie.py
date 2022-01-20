
class PrefixTree:
    class Node:
        def __init__(self, data=None, count=1):
            self.data = data
            self.count = count
            self.children = None  # {data: Node}

    def __init__(self):
        self.root = self.Node(count=0)

    def get_child(self, node, data):
        if not node.children or data not in node.children:
            return None
        return node.children[data]

    def size(self):
        return self.root.count

    def to_string(self):
        def _to_string_pre_order(node, str_list, result):
            if node:
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
        print(self.to_string(), end="")

    def add(self, prefix: list):
        if not prefix:
            raise ValueError(f"prefix cannot be empty")
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

    def contains(self, prefix: list):
        if not prefix:
            raise ValueError(f"prefix cannot be empty")
        node = self.root
        for data in prefix:
            node = self.get_child(node, data)
            if not node:
                return False
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

    def prefix_wildcard(self, prefix: list):
        def _prefix_wildcard_pre_order(node, data_list, result):
            if node:
                if node != self.root:
                    data_list.append(node.data)
                if not node.children:
                    result.append(data_list.copy())
                else:
                    for child_node in node.children.values():
                        _prefix_wildcard_pre_order(child_node, data_list, result)
                data_list.pop()
        node = self.root
        for data in prefix:
            node = self.get_child(node, data)
            if not node:
                return None
        result = list()
        _prefix_wildcard_pre_order(node, prefix[:-1:].copy(), result)
        return result   

