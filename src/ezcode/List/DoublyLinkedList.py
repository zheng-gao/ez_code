from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, PREV_NAME, FORWARD_LINK, BACKWARD_LINK, BIDIRECTION_LINK
from ezcode.List.LinkedListAlgorithm import DoublyLinkedListAlgorithm


class DoublyLinkedListPrinter:
    def __init__(self, algorithm: DoublyLinkedListAlgorithm,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        self.algorithm = algorithm
        self.forward_link = forward_link
        self.backward_link = backward_link
        self.bidirection_link = bidirection_link

    def to_string(self, node, reverse=False, include_end=True):
        if not node:
            return "None" if include_end else ""
        string, backward_node = "", self.algorithm.get_prev(node)
        while self.algorithm.has_next(node):
            data = self.algorithm.get_data(node)
            string = f"{self.bidirection_link}{data}{string}" if reverse else f"{string}{data}{self.bidirection_link}"
            node = self.algorithm.get_next(node)
        data = self.algorithm.get_data(node)
        if reverse:
            string = f"None{self.backward_link}(T) {data}{string}" if include_end else f"(T) {data}{string}"
        else:
            string = f"{string}{data} (T){self.forward_link}None" if include_end else f"{string}{data} (T)"
        if not backward_node:
            if reverse:
                return f"{string} (H){self.forward_link}None" if include_end else f"{string} (H)"
            else:
                return f"None{self.backward_link}(H) {string}" if include_end else f"(H) {string}"
        node = backward_node
        while node:
            data = self.algorithm.get_data(node)
            string = f"{string}{self.bidirection_link}{data}" if reverse else f"{data}{self.bidirection_link}{string}"
            node = self.algorithm.get_prev(node)
        if reverse:
            return f"{string} (H){self.forward_link}None" if include_end else f"{string} (H)"
        else:
            return f"None{self.backward_link}(H) {string}" if include_end else f"(H) {string}"

    def print(self, node, reverse=False, include_end=True):
        print(self.to_string(node, reverse, include_end))


class DoublyLinkedList:
    def __init__(self, head=None, tail=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME, prev_name: str = PREV_NAME):
        self.head = head
        self.tail = tail
        self.algorithm = DoublyLinkedListAlgorithm(data_name, next_name, prev_name)
        self.size = self.calculate_size(set_tail=(tail is None))

    def __len__(self):
        return self.size

    def __str__(self):
        return self.to_string()

    def calculate_size(self, set_tail=False) -> int:
        """ O(N) """
        size, node = 0, self.head
        while node:
            if set_tail and not self.algorithm.has_next(node):
                self.tail = node
            size, node = size + 1, self.algorithm.get_next(node)
        return size

    def to_string(self, reverse=False, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        printer = DoublyLinkedListPrinter(self.algorithm, forward_link, backward_link, bidirection_link)
        return printer.to_string(self.head, reverse, include_end)

    def print(self, reverse=False, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        print(self.to_string(reverse, include_end, forward_link, backward_link, bidirection_link))

    def add_to_head(self, data):
        """ O(1) """
        new_node = self.algorithm.new_node(data=data)
        self.add_node_to_head(new_node)

    def add_node_to_head(self, node):
        """ O(1) """
        if node is not None:
            self.algorithm.set_next(node=node, next_node=self.head)
            self.algorithm.set_prev(node=node, prev_node=None)
            if self.head:
                self.algorithm.set_prev(node=self.head, prev_node=node)
            else:
                self.tail = node
            self.head = node
            self.size += 1

    def add_to_tail(self, data):
        """ O(1) """
        new_node = self.algorithm.new_node(data=data, prev_node=self.tail)
        self.add_node_to_tail(new_node)

    def add_node_to_tail(self, node):
        """ O(1) """
        if node is not None:
            self.algorithm.set_next(node=node, next_node=None)
            self.algorithm.set_prev(node=node, prev_node=self.tail)
            if self.tail:
                self.algorithm.set_next(node=self.tail, next_node=node)
            else:
                self.head = node
            self.tail = node
            self.size += 1

    def peek_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Peek head at an empty DoublyLinkedList")
        return self.algorithm.get_data(self.head)

    def peek_tail(self):
        """ O(1) """
        if not self.tail:
            raise IndexError("Peek tail at an empty DoublyLinkedList")
        return self.algorithm.get_data(self.tail)

    def pop_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Pop head from an empty DoublyLinkedList")
        data = self.algorithm.get_data(self.head)
        self.head = self.algorithm.get_next(self.head)
        if self.head:
            self.algorithm.set_prev(node=self.head, prev_node=None)
        else:
            self.tail = None
        self.size -= 1
        return data

    def pop_tail(self):
        """ O(1) """
        if not self.tail:
            raise IndexError("Pop tail from an empty DoublyLinkedList")
        data = self.algorithm.get_data(self.tail)
        self.tail = self.algorithm.get_prev(self.tail)
        if self.tail:
            self.algorithm.set_next(node=self.tail, next_node=None)
        else:
            self.head = None
        self.size -= 1
        return data

    def detach_node(self, node):
        if node is not None:
            if node == self.head:
                self.head = self.algorithm.get_next(self.head)
            if node == self.tail:
                self.tail = self.algorithm.get_prev(self.tail)
            prev_node, next_node = self.algorithm.get_prev(node), self.algorithm.get_next(node)
            if next_node is not None:
                self.algorithm.set_prev(node=next_node, prev_node=prev_node)
            if prev_node is not None:
                self.algorithm.set_next(node=prev_node, next_node=next_node)
            self.size -= 1

