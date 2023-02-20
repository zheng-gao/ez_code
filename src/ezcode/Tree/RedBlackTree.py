from __future__ import annotations
from typing import Iterable
from ezcode.Tree.BinarySearchTree import BinarySearchTree


class RedBlackTree(BinarySearchTree):
    """
                    RedBlackTree                          AVLTree
     Storage        1 extra bit for color                 1 extra int for height
    Balanced        Not Strictly Balanced                 Strictly Balanced
      Search        O(logN)                               O(logN) faster
      Insert        O(logN)                               O(logN) slightly faster
    * Remove        O(logN) faster, rotations <= 3        O(logN) logN rotations, slower
    """
    def __init__(self, init_data: Iterable = None, root=None, root_copy=None):
        super().__init__(
            init_data=init_data, root=root, root_copy=root_copy,
            data_name="data", left_name="left", right_name="right"
        )

    def new_node(self, is_red: bool = True, data=None, left=None, right=None):
        node = super().new_node(data=data, left=left, right=right)
        node.__dict__["is_red"] = is_red
        return node

    def node_to_string(self, node) -> str:
        return f"{node.data}|{'R' if node.is_red else 'B'}"

    def validate(self) -> bool:
        """
        Binary Searchable.
        Root is always black.
        All NULL leaves are black, and both children of a red node are black.
        Every simple path from a given node to any of its descendant leaves contains the same number of black nodes.
        Path from root to farthest leaf is no more than twice as long as the path from the root to nearest leaf.
        """
        def _validate(node) -> tuple[bool, int, int, int]:  # is_rb_tree, max_path_length, min_path_length, black_node_count
            if node is None:
                return True, 0, 0, 0
            if node.is_red and ((node.left is not None and node.left.is_red) or (node.right is not None and node.right.is_red)):
                return False, 0, 0, 0
            left_is_rb_tree, left_max_path_length, left_min_path_length, left_black_node_count = _validate(node.left)
            if not left_is_rb_tree or (left_min_path_length << 1) < left_max_path_length:
                return False, 0, 0, 0
            right_is_rb_tree, right_max_path_length, right_min_path_length, right_black_node_count = _validate(node.right)
            if not right_is_rb_tree or (right_min_path_length << 1) < right_max_path_length:
                return False, 0, 0, 0
            if left_black_node_count != right_black_node_count:
                return False, 0, 0, 0
            max_path_length = max(left_max_path_length, right_max_path_length) + 1
            min_path_length = min(left_min_path_length, right_min_path_length) + 1
            black_node_count = left_black_node_count + (0 if node.is_red else 1)
            return True, max_path_length, min_path_length, black_node_count

        if super().validate():  # Binary Searchable
            return _validate(self.root)[0] and (self.root is None or not self.root.is_red)
        return False

    def left_rotate(self, parent, node):
        super().left_rotate(parent, node)
        self.root.is_red = False  # rotate might change the color of root

    def right_rotate(self, parent, node):
        super().right_rotate(parent, node)
        self.root.is_red = False  # rotate might change the color of root

    def insert(self, data):
        """ O(logN) """
        parents, node = self.search(data, track_parents=True)
        self.insert_node(parents, self.new_node(data=data, is_red=True))

    def insert_node(self, parents: list, node):
        if self.root is None:
            self.root = node
            self.size = 1
        else:
            super().insert_node(parent=parents[-1], node=node, is_left_node=node.data < parents[-1].data)
            self._insert_fix_up(parents, node)
        self.root.is_red = False  # fixing up red sibling process might change the color of root

    def _insert_fix_up(self, parents: list, node):
        """ O(logN) """
        parent = parents.pop()
        while parent != self.root and parent is not None and parent.is_red:  # current node is red (fix continuous red)
            grand_parent = parents.pop()  # grand_parent exists and it is black (no 2 connected red)
            uncle = grand_parent.right if parent == grand_parent.left else grand_parent.left
            if uncle is not None and uncle.is_red:  # parent & uncle -> black, grand_parent -> red
                parent.is_red, uncle.is_red, grand_parent.is_red = False, False, True  # might change the color of root
                parent, node = parents.pop(), grand_parent  # fix red grand_parent in the next round (move 2 step up!)
            else:  # uncle is black
                great_grand_parent = parents[-1] if len(parents) > 0 else None
                if parent == grand_parent.left:
                    if node == parent.right:
                        self.left_rotate(parent=grand_parent, node=parent)    # Case LR ─> Case LL
                        parent, node = node, parent  # node becomes parent.left
                    self.right_rotate(parent=great_grand_parent, node=grand_parent)  # Case LL
                    """
                          ┌────(G/B)────┐  ── left rotate P ──>   ┌───(G/B)───┐  ─swap N,P─> ...
                     ┌─(P/R)─┐      ┌─(U/B)─┐                 ┌─(N/R)─┐   ┌─(U/B)─┐
                    (x)  ┌─(N/R)─┐ (x)     (x)            ┌─(P/R)─┐  (b) (x)     (x)
                        (a)     (b)                      (x)     (a)
                    ... the node becomes a left one, LL
                              ┌───(G/B)───┐  ─right rotate G─>  ┌───(P/R)───┐   ─recolor P,G─>  ┌───(P/B)───┐
                          ┌─(P/R)─┐   ┌─(U/B)─┐             ┌─(N/R)─┐   ┌─(G/B)─┐      │    ┌─(N/R)─┐   ┌─(G/R)─┐
                     ┌─(N/R)─┐   (b) (x)     (x)           (x)     (a) (b)  ┌─(U/B)─┐  │   (x)     (a) (b)  ┌─(U/B)─┐
                    (x)     (a)                                            (x)     (x) │                   (x)     (x)
                    """                                                              # │
                else:  # parent == grand_parent.right                                  │
                    if node == parent.left:                                          # │
                        self.right_rotate(parent=grand_parent, node=parent)          # │
                        parent, node = node, parent                                  # │
                    self.left_rotate(parent=great_grand_parent, node=grand_parent)   # │
                if grand_parent == self.root:                                        # │
                    self.root = parent                                               # V
                parent.is_red, grand_parent.is_red = False, True  # node ─> black, parent ─> red, exit while loop

    def remove(self, data):
        """ O(logN) """
        self.remove_node(*self.search(data, track_parents=True))

    def remove_node(self, parents: list, node):
        """ O(logN) """
        replaced, removed = super().remove_node(parents, node)
        if removed is not None and not removed.is_red:    # removed a black node
            if replaced is not None and replaced.is_red:  # replaced with a red node
                replaced.is_red = False                   # paint it black to compensate for the removed black
            else:
                self._remove_fix_up(parents=parents, node=replaced)  # looking up for compensation

    def _remove_fix_up(self, parents: list, node):
        """ O(logN) """
        parent = parents.pop()
        grand_parent = parents.pop() if len(parents) > 0 else None
        while node != self.root and (node is None or not node.is_red):  # current node is black and the path missed a black node
            sibling = parent.right if node == parent.left else parent.left
            if sibling is not None and sibling.is_red:  # parent and the sibling's children must be black
                if node == parent.left:
                    self.left_rotate(parent=grand_parent, node=parent)  # right sibling -> left rotate P
                else:
                    self.right_rotate(parent=grand_parent, node=parent)  # left sibling -> right rotate P
                grand_parent = sibling  # after rotate, S is on top of P
                parent.is_red, sibling.is_red = True, False  # parent -> red, sibling -> black
                """
                     ┌───(P/B)────┐  -left rotate P->  ┌──(S/R)──┐  -recolor S,P->  ┌──(S/B)──┐
                 ┌─(N/B)─┐    ┌─(S/R)─┐            ┌─(P/B)─┐   (b/B)            ┌─(P/R)─┐   (b/B)
                (x)     (x) (a/B)   (b/B)      ┌─(N/B)─┐ (a/B)              ┌─(N/B)─┐ (a/B)
                                              (x)     (x)                  (x)     (x)
                subtree on N is still invalid (missing a black) but its sibling(a) becomes black
                """
            else:  # sibling is black
                if sibling.left is not None and sibling.left.is_red:
                    child = sibling.left
                    if sibling == parent.right:  # case RL
                        self.right_rotate(parent=parent, node=sibling)
                        child.is_red, sibling.is_red = False, True
                        """
                             ┌───(P/?)──────┐  -right rotate S->  ┌───(P/?)───┐  -recolor C,S->  ┌───(P/?)───┐
                         ┌─(N/B)─┐      ┌─(S/B)─┐             ┌─(N/B)─┐   ┌─(C/R)─┐          ┌─(N/B)─┐   ┌─(C/B)─┐
                        (x)     (x) ┌─(C/R)─┐  (x)           (x)     (x) (x)  ┌─(S/B)─┐     (x)     (x) (x)  ┌─(S/R)─┐
                                   (x)     (a)                               (a)     (x)                    (a)     (x)
                        subtree on C is RBT again and it becomes right-right case
                        """
                    else:  # case LL
                        self.right_rotate(parent=grand_parent, node=parent)
                        sibling.is_red, parent.is_red, child.is_red = parent.is_red, False, False
                        """
                                 ┌───(P/?)───┐  -right rotate P->  ┌──(S/B)───┐  -recolor C,S,P->  ┌───(S/?)───┐
                             ┌─(S/B)─┐   ┌─(N/B)─┐             ┌─(C/R)─┐   ┌─(P/?)─┐           ┌─(C/B)─┐   ┌─(P/B)─┐
                         ┌─(C/R)─┐  (a) (x)     (x)           (x)     (x) (a)  ┌─(N/B)─┐      (x)     (x) (a)  ┌─(N/B)─┐
                        (x)     (x)                                           (x)     (x)                     (x)     (x)
                        """
                        return  # Satisfied RBT contraints, no need to fix up
                elif sibling.right is not None and sibling.right.is_red:
                    child = sibling.right
                    if sibling == parent.right:  # case RR
                        self.left_rotate(parent=grand_parent, node=parent)
                        sibling.is_red, parent.is_red, child.is_red = parent.is_red, False, False
                        """
                             ┌───(P/?)───┐  -left rotate P->   ┌───(S/B)───┐  -recolor C,S,P->  ┌───(S/?)───┐
                         ┌─(N/B)─┐   ┌─(S/B)─┐             ┌─(P/?)─┐   ┌─(C/R)─┐            ┌─(P/B)─┐   ┌─(C/B)─┐
                        (x)     (x) (a) ┌─(C/R)─┐     ┌─(N/B)─┐   (a) (x)     (x)      ┌─(N/B)─┐   (a) (x)     (x)
                                       (x)     (x)   (x)     (x)                      (x)     (x)
                        """
                        return  # Satisfied RBT contraints, no need to fix up
                    else:  # case LR
                        self.left_rotate(parent=parent, node=sibling)
                        child.is_red, sibling.is_red = False, True
                        """
                              ┌───(P/?)─────┐  -left rotate S->   ┌───(P/?)───┐  -recolor C,S->  ┌───(P/?)───┐
                          ┌─(S/B)─┐     ┌─(N/B)─┐             ┌─(C/R)─┐   ┌─(N/B)─┐          ┌─(C/B)─┐   ┌─(N/B)─┐
                         (x) ┌─(C/R)─┐ (x)     (x)        ┌─(S/B)─┐  (x) (x)     (x)     ┌─(S/R)─┐  (x) (x)     (x)
                            (a)     (x)                  (x)     (a)                    (x)     (a)
                        subtree on C is RBT again and it becomes left-left case
                        """
                else:  # All the children of sibling are black (recolor: parent -> black, sibling -> red)
                    sibling.is_red = True
                    if parent.is_red:
                        parent.is_red = False
                        return  # Satisfied RBT contraints, no need to fix up
                    node, parent, grand_parent = parent, grand_parent, parents.pop() if len(parents) > 0 else None  # fix up on black parent
                    """
                         ┌───(P/?)────┐   -recolor P and S->   ┌───(P/B)────┐   -reset N->   ┌───(N/B)────┐
                     ┌─(N/B)─┐    ┌─(S/B)─┐                ┌─(N/B)─┐    ┌─(S/R)─┐        ┌─(x/B)─┐    ┌─(S/R)─┐
                    (x)     (x) (a/B)   (b/B)             (x)     (x) (a/B)   (b/B)     (x)     (x) (a/B)   (b/B)
                    """

    def remove_range(self, data_lower_bound, data_upper_bound):
        raise NotImplementedError

    def serialize(self, delimiter: str = ",") -> str:
        raise NotImplementedError

    def deserialize(self, formatter, string: str, delimiter: str = ","):
        raise NotImplementedError



