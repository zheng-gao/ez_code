from __future__ import annotations

from typing import Iterable

from ezcode.Tree.BinarySearchTree import BinarySearchTree


class AVLTree(BinarySearchTree):
    def __init__(self, init_data: Iterable = None, root=None, root_copy=None):
        super().__init__(
            init_data=init_data, root=root, root_copy=root_copy,
            data_name="data", left_name="left", right_name="right"
        )

    def new_node(self, height: int = 1, data=None, left=None, right=None):
        node = super().new_node(data=data, left=left, right=right)
        node.__dict__["height"] = height
        return node

    def validate(self) -> bool:
        """ Every node is balanced and binary searchable """
        def _validate(node) -> tuple[bool, int]:  # is_balanced, height
            if node is None:
                return True, 0
            left_is_balanced, left_height = _validate(node.left)
            if not left_is_balanced:
                return False, 0
            right_is_balanced, right_height = _validate(node.right)
            if not right_is_balanced:
                return False, 0
            if abs(left_height - right_height) > 1:
                return False, 0
            node_height = max(left_height, right_height) + 1
            if node.height != node_height:
                return False, 0
            return True, node_height

        if super().validate():  # Binary Searchable
            return _validate(self.root)[0]
        return False

    def node_to_string(self, node) -> str:
        return f"{node.data}|H:{node.height}|B:{self._get_balance_factor(node)}"

    def _update_height(self, node):
        if node is not None:
            height = node.height
            if node.left is None and node.right is None:
                node.height = 1
            elif node.left is not None and node.right is not None:
                node.height = max(node.left.height, node.right.height) + 1
            else:
                node.height = (node.right.height + 1) if node.left is None else (node.left.height + 1)
            return False if height == node.height else True
        return False

    def _get_balance_factor(self, node) -> int:
        if node is None:
            return 0
        left_height = 0 if node.left is None else node.left.height
        right_height = 0 if node.right is None else node.right.height
        return left_height - right_height

    def _is_balanced_node(self, node) -> bool:
        return abs(self._get_balance_factor(node)) < 2

    def _get_higher_child(self, node, prefer_left=True):
        if node is None:
            return None
        balance_factor = self._get_balance_factor(node)
        if balance_factor == 0:
            return node.left if prefer_left else node.right
        return node.left if balance_factor > 0 else node.right

    def _left_rotate(self, parent, node):
        """
        Time: O(1)
        make node the 'left' child of its right child, keep it BST
                         <----------
              (P)─┐┌─(P)              (P)─┐┌─(P)
              ┌───(R)───┐           ┌───(node)───┐
         ┌──(node)──┐  (x)         (x)       ┌──(R)──┐
        (x)        (RL)                     (RL)    (x)
        """
        right = node.right
        node.right, right.left = right.left, node
        if parent is None:
            self.root = right
        elif parent.left == node:
            parent.left = right
        else:
            parent.right = right

    def _right_rotate(self, parent, node):
        """
        Time: O(1)
        make node the 'right' child of its left child, keep it BST
                           ---------->
               (P)─┐┌─(P)              (P)─┐┌─(P)
             ┌───(node)───┐            ┌───(L)───┐
         ┌──(L)──┐       (x)          (x)   ┌──(node)──┐
        (x)     (LR)                       (LR)       (x)
        """
        left = node.left
        node.left, left.right = left.right, node
        if parent is None:
            self.root = left
        elif parent.left == node:
            parent.left = left
        else:
            parent.right = left

    def insert(self, data):
        """ Time: O(logN) """
        if self.root is None:
            self.root = self.new_node(data=data, height=1)
        else:
            parents, node = list(), self.root
            while node is not None:
                if data == node.data:
                    raise KeyError(f"{data} exist")
                parents.append(node)
                node = node.left if data < node.data else node.right
            node = self.new_node(data=data, height=1)
            parent = parents.pop()  # at least have one parent
            if data < parent.data:
                parent.left = node
            else:
                parent.right = node
            self.size += 1
            # insert fix up, time: O(logN)
            grand_parent = parents.pop() if len(parents) > 0 else None
            if parent.left is None or parent.right is None:  # else: parent has two children, no further processing is required
                is_height_updated = self._update_height(parent)  # exit while loop early if the height of parent is untouched
                while is_height_updated and grand_parent is not None and self._is_balanced_node(grand_parent):
                    node, parent, grand_parent = parent, grand_parent, parents.pop() if len(parents) > 0 else None  # search up
                    is_height_updated = self._update_height(parent)
                if is_height_updated and grand_parent is not None:  # else: not found unbalanced subtree, no further processing is required
                    great_grand_parent = parents.pop() if len(parents) > 0 else None
                    self._rebalance(great_grand_parent, grand_parent, parent, node)

    def _rebalance(self, great_grand_parent, grand_parent, parent, node):
        """ Time: O(1) """
        if parent == grand_parent.left:
            if node == parent.right:  # Case LR
                self._left_rotate(parent=grand_parent, node=parent)  # convert to case LL
                """
                LR: Assume S had height H and node has been removed from subtree-S
                                   (GG)─┐┌─(GG)    -- left rotate P -->           (GG)─┐┌─(GG)
                                 ┌────(G|H+2)────┐                              ┌────(G|H+2)────┐
                      ┌───────(P|H+1)──────┐  (S|H|-1)                  ┌─────(N|H)─────┐    (S|H|-1)
                 ┌─(A|H-1)─┐         ┌───(N|H)───┐               ┌───(P|H+1)───┐   (C|H-1/H-2)
                (x)         (x) (B|H-1/H-2) (C|H-1/H-2)     ┌─(A|H-1)─┐   (B|H-1/H-2)
                                                           (x)       (x)
                -- right rotate G -->
                                   (G)─┐┌─(G)
                            ┌─────────(N|H)─────────┐          <------------------------ increase N.height
                      ┌──(P|H+1)──┐           ┌──(G|H+2)──┐    <------------------------ decrease P/G.height
                 ┌─(A|H-1)─┐ (B|H-1/H-2) (C|H-1/H-2)   (S|H|-1)                                     |
                (x)       (x)                                                                       |
                N=H, A=H-1: (if A=H, choose A as N and go to case LL)                               |
                update: G=H+2 -> H                                                                  |
                update: P=H+1 -> H                                                                  |
                update: N=H   -> H+1 < G's original height "H+2", fixing up                         |
                                                                                                    |
                Insert LR: Assume S has height H and node has been added to subtree-N               |
                                  (GG)─┐┌─(GG)      -- left rotate P -->      (GG)─┐┌─(GG)          |
                               ┌─────(G|H+2)─────┐                          ┌────(G|H+2)────┐       |
                      ┌───(P|H+1|+1)───┐       (S|H)                 ┌───(N|H|+1)───┐     (S|H)     |
                 ┌─(A|H)─┐       ┌──(N|H|+1)──┐               ┌──(P|H+1|+1)──┐ (C|H-1|/+1)          |
                (x)     (x) (B|H-1|/+1)  (C|H-1|/+1)      ┌─(A|H)─┐     (B|H-1|/+1)                 |
                                                         (x)     (x)                                |
                -- right rotate G -->                                                               |
                                         (GG)─┐┌─(GG)                                               |
                                    ┌───────(N|H|+1)───────┐            <--------------- increase N.height
                              ┌─(P|H+1|+1)─┐         ┌───(G|H+2)───┐    <--------------- decrease P/G.height
                          ┌─(A|H)─┐  (B|H-1|/+1) (C|H-1|/+1)     (S|H)                              |
                         (x)     (x)                                                                |
                """                                                                               # |
            self._right_rotate(parent=great_grand_parent, node=grand_parent)  # case LL             |
            """                                                                                     |
            Remove LL: Assume S had height H and node has been removed from subtree-S               |
                      (GG)─┐┌─(GG) -- right rotate G --> (GG)─┐┌─(GG)                               |
                      ┌──(G|H+2)──┐                    ┌────(P|H+1)────┐        <----------- update P.height
                 ┌─(P|H+1)─┐   (S|H|-1)           ┌─(N|H)─┐      ┌─(G|H+2)─┐    <----------- update G.height
             ┌─(N|H)─┐ (A|H/H-1)                 (x)     (x) (A|H/H-1)  (S|H|-1)                    |
            (x)      (x)                                                                            |
            A=H:                            A=H-1:                                                  |
            update: G=H+2 -> H+1            update: G=H+2 -> H                                      |
            update: P=H+1 -> H+2, fixed     update: P=H+1 -> H+1 < G's original height, fixing up   |
                                                                                                    |
            Insert LL: Assume S has height H and node has been added to subtree-N                   |
                         (GG)─┐┌─(GG)  -- right rotate G -->  (GG)─┐┌─(GG)                          |
                        ┌──(G|H+2)──┐                       ┌───(P|H+1|+1)───┐  <---- same height   |
                  ┌─(P|H+1|+1)─┐  (S|H)                ┌─(N|H|+1)─┐     ┌─(G|H+2)─┐  <---- decrease G.height
             ┌─(N|H|+1)─┐    (A|H)                  (x)          (x)  (A|H)     (S|H)               |
            (x)        (x)                                                                          |
            """                                                                                   # |
        else:                                                                                     # |
            if node == parent.left:  # Case RL                                                      |
                self._right_rotate(parent=grand_parent, node=parent)  # convert to case RR          |
            self._left_rotate(parent=great_grand_parent, node=grand_parent)  # case RR              |
        self._update_height(grand_parent)  # use update to fit both insert/remote fixes  <----------|
        self._update_height(parent)
        self._update_height(node)

    def remove(self, data):
        """ Time: O(logN) """
        parents, node = self.search(data, track_parents=True)
        self.remove_node(parents=parents, node=node)

    def remove_node(self, parents, node):
        """ Time: O(logN) """
        if node is not None:
            if node.right is None:
                parent = parents.pop() if len(parents) > 0 else None
                if node == self.root:
                    self.root = node.left
                else:
                    if node == parent.left:
                        parent.left = node.left
                    else:
                        parent.right = node.left
            else:
                parents.append(node)
                left_most = node.right             # left most node of the right tree
                while left_most.left is not None:  # left_most only have the right child
                    parents.append(left_most)
                    left_most = left_most.left
                left_most.data, node.data = node.data, left_most.data  # swap data then delete left most
                parent = parents.pop()  # at least has one parent
                if left_most == parent.right:
                    parent.right = left_most.right
                else:
                    parent.left = left_most.right
            self.size -= 1
            # remove fix up, time: O(logN)
            grand_parent = parent
            while grand_parent is not None:
                is_height_updated = self._update_height(grand_parent)
                while grand_parent is not None:
                    if self._is_balanced_node(grand_parent):
                        if not is_height_updated:
                            return
                        grand_parent = parents.pop() if len(parents) > 0 else None  # search up for unbalanced node
                        is_height_updated = self._update_height(grand_parent)
                    else:
                        break
                if grand_parent is not None:
                    great_grand_parent = parents.pop() if len(parents) > 0 else None
                    parent = self._get_higher_child(grand_parent)  # parent/node cannot be None since grand_parent is unbalanced
                    node = self._get_higher_child(parent, prefer_left=(parent == grand_parent.left))
                    self._rebalance(great_grand_parent, grand_parent, parent, node)
                    grand_parent = great_grand_parent

#     def __eq__(self, other) -> bool:
#         def _tree_equal(node_1, node_2):
#             if node_1 is None and node_2 is None:
#                 return True
#             if node_1 is None or node_2 is None:
#                 return False
#             if node_1.data != node_2.data or node_1.height != node_2.height:
#                 return False
#             return _tree_equal(node_1.left, node_2.left) and _tree_equal(node_1.right, node_2.right)
#
#         if type(other) != self.__class__:
#             return False
#         return _tree_equal(self.root, other.root)
#
#     def copy_tree(self, node):
#         if node is None:
#             return None, 0
#         if not (self.root is None and self.new_node().match(node)) and not self.root.match(node):
#             raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
#         root_copy, size_copy = self.copy_node(node), 0
#         queue, queue_copy = deque([node]), deque([root_copy])
#         while len(queue) > 0:
#             node = queue.popleft()
#             node_copy = queue_copy.popleft()
#             size_copy += 1
#             if node.left is not None:
#                 node_copy.left = self.copy_node(node.left)
#                 queue.append(node.left)
#                 queue_copy.append(node_copy.left)
#             if node.right is not None:
#                 node_copy.right = self.copy_node(node.right)
#                 queue.append(node.right)
#                 queue_copy.append(node_copy.right)
#         return root_copy, size_copy
#
#     def copy(self):
#         tree = self.__class__()
#         tree.root, tree.size = self.copy_tree(self.root)
#         return tree






