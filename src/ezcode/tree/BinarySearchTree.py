from ezcode.Tree.BinaryTree import DATA_NAME, LEFT_NAME, RIGHT_NAME, BinaryTree, BinaryTreeIterator


class BinarySearchTree(BinaryTree):
    def __init__(self,
        init_data=None, root=None,
        data_name=DATA_NAME, left_name=LEFT_NAME, right_name=RIGHT_NAME
    ):
        super().__init__(
            root=root, data_name=data_name, left_name=left_name, right_name=right_name,
            iterator_mode=BinaryTreeIterator.Mode.IN_ORDER, iterator_is_left_first=True
        )
        if init_data is not None:
            for data in init_data:
                self.insert(data)

    def __contains__(self, data) -> bool:
        return self.search(data) is not None

    def validate(self) -> bool:
        def _validate(node, left_most_node, right_most_node, lower_bound, upper_bound) -> bool:
            if node is None:
                return True
            if (node != left_most_node and not (lower_bound < node.data)) or (node != right_most_node and not (node.data < upper_bound)):
                return False  # node.data should be within boundaries
            valid_left = _validate(node.left, left_most_node, right_most_node, lower_bound, node.data)
            valid_right = _validate(node.right, left_most_node, right_most_node, node.data, upper_bound)
            return valid_left and valid_right

        if self.root is None:
            return True
        left_most_node = self.get_left_most(self.root)
        right_most_node = self.get_right_most(self.root)
        return _validate(self.root, left_most_node, right_most_node, left_most_node.data, right_most_node.data)

    def search(self, data, return_with_parent=False):
        """ O(logN) """
        parent, node = None, self.root
        while node is not None:
            if data == node.data:
                break
            parent, node = node, node.left if data < node.data else node.right
        return (parent, node) if return_with_parent else node

    def insert(self, data):
        """ O(logN) """
        if self.root is None:
            self.root = self.new_node(data=data)
            return
        parent, node = None, self.root
        while node is not None:
            if data == node.data:
                raise KeyError(f"{data} exist")
            parent, node = node, node.left if data < node.data else node.right
        node = self.new_node(data=data)
        if data < parent.data:
            parent.left = node
        else:
            parent.right = node

    def remove(self, data):
        """ O(logN) """
        parent, node = self.search(data, return_with_parent=True)
        self.remove_node(parent, node)

    def remove_node(self, parent, node):
        """ O(logN) """
        if node is not None:
            if node.right is None:
                if node == self.root:
                    self.root = node.left
                elif node == parent.left:
                    parent.left = node.left
                else:
                    parent.right = node.left
            else:  # left most node of the right tree
                left_most_parent, left_most = node, node.right
                while left_most.left is not None:  # left_most only have the right child
                    left_most_parent, left_most = left_most, left_most.left
                left_most.data, node.data = node.data, left_most.data  # swap data then delete left most
                if left_most_parent == node:  # never move
                    left_most_parent.right = left_most.right  # left_most only have the right child
                else:
                    left_most_parent.left = left_most.right

    def remove_range(self, data_lower_bound, data_upper_bound):
        if data_upper_bound < data_lower_bound:
            raise ValueError(f"data_upper_bound {data_upper_bound} is smaller than data_lower_bound {data_lower_bound}")
        parent, node = None, self.root
        while node is not None:
            print(node.data)
            if node.data < data_lower_bound:
                parent, node = node, node.right
            elif data_upper_bound < node.data:
                parent, node = node, node.left
            else:
                if node.right is None:
                    if node == self.root:
                        self.root = node.left
                    elif node == parent.left:
                        parent.left = node.left
                    else:
                        parent.right = node.left
                    node = node.left
                else:  # left_most only have the right child
                    left_most_parent, left_most = node, node.right
                    while left_most.left is not None:  # left_most only have the right child
                        left_most_parent, left_most = left_most, left_most.left
                    left_most.data, node.data = node.data, left_most.data  # swap data then delete left most
                    if left_most_parent == node:  # never move
                        left_most_parent.right = left_most.right  # left_most only have the right child
                    else:
                        left_most_parent.left = left_most.right


