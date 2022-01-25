from ezcode.list.const import DATA_NAME, NEXT_NAME, PREV_NAME


class SinglyLinkedListAlgorithm:
    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.data_name = data_name
        self.next_name = next_name

    def new_node(self, data=None, next_node=None):
        node = self.FakeNode()
        node.__dict__ = {self.data_name: data, self.next_name: next_node}
        return node

    def has_next(self, node, steps: int = 1) -> bool:
        if not node:
            return False
        next_node = node
        for _ in range(steps):
            next_node = next_node.__dict__[self.next_name]
            if not next_node:
                return False
        return True

    def get_next(self, node, steps: int = 1):
        next_node = node
        for _ in range(steps):
            next_node = next_node.__dict__[self.next_name]
        return next_node

    def set_next(self, node, next_node=None):
        node.__dict__[self.next_name] = next_node

    def get_data(self, node):
        return node.__dict__[self.data_name]

    def reverse(self, previous_node, current_node):
        """ head = reverse(head, head.next) """
        if current_node:
            head = self.reverse(current, self.get_next(current))
            self.set_next(node=current, next_node=previous)
            self.set_next(node=previous, next_node=None)
            return head
        else:
            return previous


class DoublyLinkedListAlgorithm:
    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, data_name: str = DATA_NAME, next_name: str = NEXT_NAME, prev_name: str = PREV_NAME):
        self.data_name = data_name
        self.next_name = next_name
        self.prev_name = prev_name

    def new_node(self, data=None, next_node=None, prev_node=None):
        node = self.FakeNode()
        node.__dict__ = {self.data_name: data, self.next_name: next_node, self.prev_name: prev_node}
        return node

    def has_next(self, node, steps: int = 1) -> bool:
        if not node:
            return False
        next_node = node
        for _ in range(steps):
            next_node = next_node.__dict__[self.next_name]
            if not next_node:
                return False
        return True

    def has_prev(self, node, steps: int = 1) -> bool:
        if not node:
            return False
        prev_node = node
        for _ in range(steps):
            prev_node = prev_node.__dict__[self.prev_name]
            if not prev_node:
                return False
        return True

    def get_next(self, node, steps: int = 1):
        next_node = node
        for _ in range(steps):
            next_node = next_node.__dict__[self.next_name]
        return next_node

    def get_prev(self, node, steps: int = 1):
        prev_node = node
        for _ in range(steps):
            prev_node = prev_node.__dict__[self.prev_name]
        return prev_node

    def set_next(self, node, next_node=None):
        node.__dict__[self.next_name] = next_node

    def set_prev(self, node, prev_node=None):
        node.__dict__[self.prev_name] = prev_node

    def get_data(self, node):
        return node.__dict__[self.data_name]

