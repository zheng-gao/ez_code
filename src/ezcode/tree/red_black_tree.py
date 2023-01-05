from ezcode.tree.binary_tree import BinaryTree


class RedBlackTree(BinaryTree):
    def __init__(self, root=None):
        super().__init__(root=root, data_name="data", left_name="left", right_name="right", algorithm=None)

    def new_node(self, data, is_red=True, parent=None, left=None, right=None):
        node = super().new_node(data, left, right)
        node.__dict__.update({"is_red": is_red, "parent": parent})
        return node

    def node_to_string(self, node):
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
            if (node.left is not None and node.left.data >= node.data) or (node.right is not None and node.right.data <= node.data):
                return False, 0, 0, 0
            left_is_rb_tree, left_max_path_length, left_min_path_length, left_black_node_count = _validate(node.left)
            if not left_is_rb_tree or left_max_path_length > (left_min_path_length << 1):
                return False, 0, 0, 0
            right_is_rb_tree, right_max_path_length, right_min_path_length, right_black_node_count = _validate(node.right)
            if not right_is_rb_tree or right_max_path_length > (right_min_path_length << 1):
                return False, 0, 0, 0
            if left_black_node_count != right_black_node_count:
                return False, 0, 0, 0
            max_path_length = max(left_max_path_length, right_max_path_length) + 1
            min_path_length = min(left_min_path_length, right_min_path_length) + 1
            black_node_count = left_black_node_count + (0 if node.is_red else 1)
            return True, max_path_length, min_path_length, black_node_count

        if self.root is None:
            return True
        if self.root.is_red:
            return False
        return _validate(self.root)[0]

    def _rotate(self, node, is_left_rotation=True):
        """ O(1) """
        parent = node.parent
        if is_left_rotation:
            """
            left rotate: O(1)
            make node the 'left' child of its right child, keep it BST
                             <----------
                  (P)─┐┌─(P)              (P)─┐┌─(P)
                  ┌───(R)───┐           ┌───(node)───┐
             ┌──(node)──┐  (x)         (x)       ┌──(R)──┐
            (x)        (RL)                     (RL)    (x)
            """
            right, right_left = node.right, node.right.left
            node.right = right_left
            if right_left is not None:
                right_left.parent = node
            right.left, node.parent, right.parent = node, right, parent
            if parent is None:
                self.root = right  # might change the color of root
            elif parent.left == node:
                parent.left = right
            else:
                parent.right = right
        else:
            """
            right rotate: O(1)
            make node the 'right' child of its left child, keep it BST
                               ---------->
                   (P)─┐┌─(P)              (P)─┐┌─(P)
                 ┌───(node)───┐            ┌───(L)───┐
             ┌──(L)──┐       (x)          (x)   ┌──(node)──┐
            (x)     (LR)                       (LR)       (x)
            """
            left, left_right = node.left, node.left.right
            node.left = left_right
            if left_right is not None:
                left_right.parent = node
            left.right, node.parent, left.parent = node, left, parent
            if parent is None:
                self.root = left  # might change the color of root
            elif parent.left == node:
                parent.left = left
            else:
                parent.right = left
        self.root.is_red = False  # root is black

    def insert(self, data):
        """ O(logN) """
        if self.root is None:
            self.root = self.new_node(data=data, is_red=False)  # root is black
            return
        parent, node = None, self.root
        while node is not None:
            if data == node.data:
                raise KeyError(f"{data} exist")
            parent, node = node, node.left if data < node.data else node.right
        node = self.new_node(data=data, is_red=True, parent=parent)
        if data < parent.data:
            parent.left = node
        else:
            parent.right = node
        self._insert_fix_up(node=parent, child=node)

    def _insert_fix_up(self, node, child):
        """ O(logN) """
        while node != self.root and node is not None and node.is_red:  # current node is red (fix continuous red)
            parent = node.parent  # parent exists and it is black (no 2 connected red)
            sibling = parent.right if node == parent.left else parent.left
            if sibling is not None and sibling.is_red:  # node & sibling -> black, parent -> red
                node.is_red, sibling.is_red, parent.is_red = False, False, True  # might change the color of root
                node, child = parent.parent, parent  # fix red parent in the next round (move up 2 steps!)
            else:  # sibling is black
                if node == parent.left:
                    if child == node.right:
                        self._rotate(node=node, is_left_rotation=True)
                        node, child = child, node  # child becomes node.left
                    self._rotate(node=parent, is_left_rotation=False)
                    """
                          ┌────(P/B)────┐    -left rotate N->     ┌───(P/B)───┐  -swap C,N-> ...
                     ┌─(N/R)─┐      ┌─(S/B)─┐                 ┌─(C/R)─┐   ┌─(S/B)─┐
                    (x)  ┌─(C/R)─┐ (x)     (x)            ┌─(N/R)─┐  (b) (x)     (x)
                        (a)     (b)                      (x)     (a)
                    ... the child becomes a left node
                              ┌───(P/B)───┐  -right rotate P->  ┌───(N/R)───┐  -recolor N,P->  ┌───(N/B)───┐
                          ┌─(N/R)─┐   ┌─(S/B)─┐             ┌─(C/R)─┐   ┌─(P/B)─┐          ┌─(C/R)─┐   ┌─(P/R)─┐
                     ┌─(C/R)─┐   (b) (x)     (x)           (x)     (a) (b)  ┌─(S/B)─┐     (x)     (a) (b)  ┌─(S/B)─┐
                    (x)     (a)                                            (x)     (x)                    (x)     (x)
                    """
                else:  # node == parent.right                                                               |
                    if child == node.left:                                                                # |
                        self._rotate(node=node, is_left_rotation=False)                                   # |
                        node, child = child, node                                                         # |
                    self._rotate(node=parent, is_left_rotation=True)                                      # |
                if parent == self.root:                                                                   # |
                    self.root = node                                                                      # |
                node.is_red, parent.is_red = False, True  # node -> black, parent -> red, exit while loop <─┘
        self.root.is_red = False  # red sibling process might change the color of root

    def get_node(self, data):
        """ O(logN) """
        node = self.root
        while node is not None:
            if data == node.data:
                break
            node = node.left if data < node.data else node.right
        return node

    def remove(self, data):
        """ O(logN) """
        node = self.get_node(data)
        if node is None:
            return
        if node.right is None:
            if node == self.root:
                self.root = node.left
                if node.left is not None:
                    node.left.parent = None
                if self.root is not None:
                    self.root.is_red = False
                return
            elif node == node.parent.left:
                node.parent.left = node.left
                if node.left is not None:
                    node.left.parent = node.parent
            else:
                node.parent.right = node.left
                if node.left is not None:
                    node.left.parent = node.parent
            if not node.is_red:                                # deleted a black node
                if node.left is None or not node.left.is_red:  # missing a black node
                    self._remove_fix_up(parent=node.parent, node=node.left)
                else:
                    node.left.is_red = False
        else:
            left_most = node.right             # left most node of the right tree
            while left_most.left is not None:  # left_most only have the right child
                left_most = left_most.left
            left_most.data, node.data = node.data, left_most.data  # swap data then delete left most, color untouched
            if left_most == node.right:
                node.right = left_most.right
                if left_most.right is not None:
                    left_most.right.parent = node
            else:
                left_most.parent.left = left_most.right
                if left_most.right is not None:
                    left_most.right.parent = left_most.parent
            if not left_most.is_red:                                       # deleted a black node
                if left_most.right is None or not left_most.right.is_red:  # missing a black node
                    self._remove_fix_up(parent=left_most.parent, node=left_most.right)
                else:
                    left_most.right.is_red = False

    def _remove_fix_up(self, parent, node):
        """ O(logN) """
        while node != self.root and (node is None or not node.is_red):  # current node is black and the path missed a black node
            if node is not None:
                parent = node.parent
            sibling = parent.right if node == parent.left else parent.left
            if sibling is not None and sibling.is_red:  # parent and the sibling's children must be black
                self._rotate(node=parent, is_left_rotation=True)
                parent.is_red, sibling.is_red = True, False  # parent -> red, sibling -> black
                """
                     ┌───(P/B)────┐  -left rotate P->  ┌──(S/R)──┐  -recolor S,P->  ┌──(S/B)──┐
                 ┌─(N/B)─┐    ┌─(S/R)─┐            ┌─(P/B)─┐   (b/B)            ┌─(P/R)─┐   (b/B)
                (x)     (x) (a/B)   (b/B)      ┌─(N/B)─┐ (a/B)              ┌─(N/B)─┐ (a/B)
                                              (x)     (x)                  (x)     (x)
                subtree on N is still invalid(missing a black) but its sibling(a) becomes black
                """
            else:  # sibling is black
                if sibling.left is not None and sibling.left.is_red:
                    child = sibling.left
                    if sibling == parent.right:  # right-left case
                        self._rotate(node=sibling, is_left_rotation=False)
                        child.is_red, sibling.is_red = False, True
                        """
                             ┌───(P/?)──────┐  -right rotate S->  ┌───(P/?)───┐  -recolor C,S->  ┌───(P/?)───┐
                         ┌─(N/B)─┐      ┌─(S/B)─┐             ┌─(N/B)─┐   ┌─(C/R)─┐          ┌─(N/B)─┐   ┌─(C/B)─┐
                        (x)     (x) ┌─(C/R)─┐  (x)           (x)     (x) (x)  ┌─(S/B)─┐     (x)     (x) (x)  ┌─(S/R)─┐
                                   (x)     (a)                               (a)     (x)                    (a)     (x)
                        subtree on C is RBT again and it becomes right-right case
                        """
                    else:  # left-left case
                        self._rotate(node=parent, is_left_rotation=False)
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
                    if sibling == parent.right:  # right-right case
                        self._rotate(node=parent, is_left_rotation=True)
                        sibling.is_red, parent.is_red, child.is_red = parent.is_red, False, False
                        """
                             ┌───(P/?)───┐  -left rotate P->   ┌───(S/B)───┐  -recolor C,S,P->  ┌───(S/?)───┐
                         ┌─(N/B)─┐   ┌─(S/B)─┐             ┌─(P/?)─┐   ┌─(C/R)─┐            ┌─(P/B)─┐   ┌─(C/B)─┐
                        (x)     (x) (a) ┌─(C/R)─┐     ┌─(N/B)─┐   (a) (x)     (x)      ┌─(N/B)─┐   (a) (x)     (x)
                                       (x)     (x)   (x)     (x)                      (x)     (x)
                        """
                        return  # Satisfied RBT contraints, no need to fix up
                    else:  # left-right case
                        self._rotate(node=sibling, is_left_rotation=True)
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
                    node = parent  # fix up if parent was black
                    """
                         ┌───(P/?)────┐   -recolor P and S->   ┌───(P/B)────┐   -reset N->   ┌───(N/B)────┐
                     ┌─(N/B)─┐    ┌─(S/B)─┐                ┌─(N/B)─┐    ┌─(S/R)─┐        ┌─(x/B)─┐    ┌─(S/R)─┐
                    (x)     (x) (a/B)   (b/B)             (x)     (x) (a/B)   (b/B)     (x)     (x) (a/B)   (b/B)
                    """

