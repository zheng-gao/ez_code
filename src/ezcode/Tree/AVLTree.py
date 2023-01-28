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

    def insert_node(self, parents: list, node):
        if self.root is None:
            self.root = node
            self.size = 1
        else:
            super().insert_node(parent=parents[-1], node=node, is_left_node=node.data < parents[-1].data)
            self._insert_fix_up(parents, node)

    def insert(self, data):
        """ Time: O(logN) """
        parents, node = self.search(data, track_parents=True)
        self.insert_node(parents, self.new_node(data=data, height=1))

    def _insert_fix_up(self, parents, node):
        parent = parents.pop()
        if parent is not None:
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
                self.left_rotate(parent=grand_parent, node=parent)  # convert to case LL
                """
                Remove LR: Assume S had height H and node has been removed from subtree-S
                                   (GG)─┐┌─(GG)    ── left rotate P ──>           (GG)─┐┌─(GG)
                                 ┌────(G|H+2)────┐                              ┌────(G|H+2)────┐
                      ┌───────(P|H+1)──────┐  (S|H|-1)                  ┌─────(N|H)─────┐    (S|H|-1)
                 ┌─(A|H-1)─┐         ┌───(N|H)───┐               ┌───(P|H+1)───┐   (C|H-1/H-2)
                (x)         (x) (B|H-1/H-2) (C|H-1/H-2)     ┌─(A|H-1)─┐   (B|H-1/H-2)
                                                           (x)       (x)
                ── right rotate G ──>
                                   (G)─┐┌─(G)
                            ┌─────────(N|H)─────────┐          <────────────────────────── update N.height
                      ┌──(P|H+1)──┐           ┌──(G|H+2)──┐    <────────────────────────── update P/G.height
                 ┌─(A|H-1)─┐ (B|H-1/H-2) (C|H-1/H-2)   (S|H|-1)                                     │
                (x)       (x)                                                                       │
                N=H, A=H-1: (if A=H, choose A as N and go to case LL)                               │
                update: G=H+2 -> H                                                                  │
                update: P=H+1 -> H                                                                  │
                update: N=H   -> H+1 < G's original height "H+2", fixing up                         │
                                                                                                    │
                Insert LR: Assume S has height H and node has been added to subtree-N               │
                                  (GG)─┐┌─(GG)      ── left rotate P ──>      (GG)─┐┌─(GG)          │
                               ┌─────(G|H+2)─────┐                          ┌────(G|H+2)────┐       │
                      ┌───(P|H+1|+1)───┐       (S|H)                 ┌───(N|H|+1)───┐     (S|H)     │
                 ┌─(A|H)─┐       ┌──(N|H|+1)──┐               ┌──(P|H+1|+1)──┐ (C|H-1|/+1)          │
                (x)     (x) (B|H-1|/+1)  (C|H-1|/+1)      ┌─(A|H)─┐     (B|H-1|/+1)                 │
                                                         (x)     (x)                                │
                ── right rotate G ──>                                                               │
                                         (GG)─┐┌─(GG)                                               │
                                    ┌───────(N|H|+1)───────┐            <─────────────── increase N.height
                              ┌─(P|H+1|+1)─┐         ┌───(G|H+2)───┐    <─────────────── decrease P/G.height
                          ┌─(A|H)─┐  (B|H-1|/+1) (C|H-1|/+1)     (S|H)                              │
                         (x)     (x)                                                                │
                """                                                                               # │
            self.right_rotate(parent=great_grand_parent, node=grand_parent)  # case LL              │
            """                                                                                     │
            Remove LL: Assume S had height H and node has been removed from subtree-S               │
                      (GG)─┐┌─(GG) ── right rotate G ──> (GG)─┐┌─(GG)                               │
                      ┌──(G|H+2)──┐                    ┌────(P|H+1)────┐        <─────────── update P.height
                 ┌─(P|H+1)─┐   (S|H|-1)           ┌─(N|H)─┐      ┌─(G|H+2)─┐    <─────────── update G.height
             ┌─(N|H)─┐ (A|H/H-1)                 (x)     (x) (A|H/H-1)  (S|H|-1)                    │
            (x)      (x)                                                                            │
            A=H:                            A=H-1:                                                  │
            update: G=H+2 -> H+1            update: G=H+2 -> H                                      │
            update: P=H+1 -> H+2, fixed     update: P=H+1 -> H+1 < G's original height, fixing up   │
                                                                                                    │
            Insert LL: Assume S has height H and node has been added to subtree-N                   │
                         (GG)─┐┌─(GG)  ── right rotate G ──>  (GG)─┐┌─(GG)                          │
                        ┌──(G|H+2)──┐                       ┌───(P|H+1|+1)───┐  <──── same height   │
                  ┌─(P|H+1|+1)─┐  (S|H)                ┌─(N|H|+1)─┐     ┌─(G|H+2)─┐  <──── decrease G.height
             ┌─(N|H|+1)─┐    (A|H)                  (x)          (x)  (A|H)     (S|H)               │
            (x)        (x)                                                                          │
            """                                                                                   # │
        else:                                                                                     # │
            if node == parent.left:  # Case RL                                                      │
                self.right_rotate(parent=grand_parent, node=parent)  # convert to case RR           │
            self.left_rotate(parent=great_grand_parent, node=grand_parent)  # case RR               │
        self._update_height(grand_parent)  # use update to fit both insert/remove fixes  <──────────┘
        self._update_height(parent)
        self._update_height(node)

    def remove(self, data):
        """ Time: O(logN) """
        self.remove_node(*self.search(data, track_parents=True))

    def remove_node(self, parents: list, node):
        """ Time: O(logN) """
        super().remove_node(parents, node)
        grand_parent = parents.pop()
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

    def remove_range(self, data_lower_bound, data_upper_bound):
        raise NotImplementedError

    def serialize(self, delimiter: str = ",") -> str:
        raise NotImplementedError

    def deserialize(self, formatter, string: str, delimiter: str = ","):
        raise NotImplementedError

