from ezcode.list.const import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.list.algorithm import SinglyLinkedListAlgorithm


class SinglyLinkedListPrinter:
    def __init__(self, algorithm: SinglyLinkedListAlgorithm, forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK):
        self.algorithm = algorithm
        self.forward_link = forward_link
        self.backward_link = backward_link

    def to_string(self, node, reverse=False):
        string, link = "", self.forward_link if not reverse else self.backward_link
        while node and self.algorithm.has_next(node):
            string += f"{self.algorithm.get_data(node)}{link}"
            node = self.algorithm.get_next(node)
        if node:
            string += f"{self.algorithm.get_data(node)}{link}"
        print("None")

    def print(self, node, reverse=False):
        print(self.to_string(node, reverse))
