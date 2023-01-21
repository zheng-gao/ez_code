from collections import deque
from enum import Enum

from ezcode.Tree import DATA_NAME, LEFT_NAME, RIGHT_NAME


class BinaryTreeIterator:
    Mode = Enum("Mode", ["DFS", "BFS", "PRE_ORDER", "IN_ORDER", "POST_ORDER"])

    def __init__(self, node=None, mode: Mode = Mode.DFS, is_left_first: bool = True,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME
    ):
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.child_selector = self._left_first if is_left_first else self._right_first
        if mode == BinaryTreeIterator.Mode.DFS or mode == BinaryTreeIterator.Mode.PRE_ORDER:
            self.generator = self._pre_order(node)
        elif mode == BinaryTreeIterator.Mode.IN_ORDER:
            self.generator = self._in_order(node)
        elif mode == BinaryTreeIterator.Mode.POST_ORDER:
            self.generator = self._post_order(node)
        else:  # BFS
            self.generator = self._bfs(node)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generator).__dict__[self.data_name]

    def _left_first(self, node):
        if node is not None:
            yield node.__dict__[self.left_name]
            yield node.__dict__[self.right_name]

    def _right_first(self, node):
        if node is not None:
            yield node.__dict__[self.right_name]
            yield node.__dict__[self.left_name]

    def _pre_order(self, node):
        if node is not None:
            yield node
            for child in self.child_selector(node):
                yield from self._pre_order(child)

    def _in_order(self, node):
        if node is not None:
            can_yield = True
            for child in self.child_selector(node):
                yield from self._in_order(child)
                if can_yield:
                    yield node
                can_yield = False

    def _post_order(self, node):
        if node is not None:
            for child in self.child_selector(node):
                yield from self._post_order(child)
            yield node

    # def _bfs(self, node, depth=0):
    #     if node is not None and depth < self.height:  # self.height need a scan of the whole tree
    #         yield node
    #         for child in self._bfs(node, depth + 1):
    #             yield from self.child_selector(child)
    def _bfs(self, node):
        if node is not None:
            queue = deque([node])
            while len(queue) > 0:
                node = queue.popleft()
                yield node
                for child in self.child_selector(node):
                    if child is not None:
                        queue.append(child)

