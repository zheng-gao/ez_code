from typing import Callable

from ezcode.tree.binary_tree import BinaryTree


class SegmentTree(BinaryTree):
    """
        SegmentTree is Complete
        Suitable for repeated queries
        Cannot add or delete items once the tree is built
    """
    def __init__(self, merge: Callable = lambda x, y: x + y, data_list: list = None):
        super().__init__(root=None, data_name="data", left_name="left", right_name="right", algorithm=None)
        self.merge = merge  # sum, max, min, gcd or lambda x, y: ...
        if data_list:
            self.build_tree(data_list=data_list)

    def new_node(self, start: int, end: int, data, left=None, right=None):
        node = super().new_node(data, left, right)
        node.__dict__.update({"start": start, "end": end})
        return node

    def node_to_string(self, node):
        return f"[{node.start},{node.end}]:" + str(node.data)

    def build_tree(self, data_list: list):
        """ Time: O(N), Space: O(N) """
        def build_tree_helper(start: int, end: int):
            if start == end:
                return self.new_node(start=start, end=end, data=data_list[start])
            mid = start + (end - start) // 2
            left, right = build_tree_helper(start, mid), build_tree_helper(mid + 1, end)  # left include mid
            return self.new_node(start, end, self.merge(left.data, right.data), left, right)

        self.root = build_tree_helper(0, len(data_list) - 1)

    def update(self, index: int, data):
        """ Time: O(logN) """
        def update_helper(node, index: int, data):
            if node.start == node.end == index:
                node.data = data
                return
            mid = node.start + (node.end - node.start) // 2
            if index <= mid:  # left include mid
                update_helper(node.left, index, data)
            else:
                update_helper(node.right, index, data)
            node.data = self.merge(node.left.data, node.right.data)

        update_helper(self.root, index, data)

    def query(self, start: int, end: int):
        """ Time: O(logN) """
        def query_helper(node, start: int, end: int):
            if node.start == start and node.end == end:
                return node.data
            mid = node.start + (node.end - node.start) // 2
            if end <= mid:  # left include mid
                return query_helper(node.left, start, end)
            if start > mid:
                return query_helper(node.right, start, end)
            return self.merge(
                query_helper(node.left, start, mid),
                query_helper(node.right, mid + 1, end)
            )

        return query_helper(self.root, start, end)
