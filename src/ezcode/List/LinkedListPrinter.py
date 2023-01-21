from ezcode.List import FORWARD_LINK, BACKWARD_LINK, BIDIRECTION_LINK
from ezcode.List.LinkedListAlgorithm import SinglyLinkedListAlgorithm, DoublyLinkedListAlgorithm


class SinglyLinkedListPrinter:
    def __init__(self, algorithm: SinglyLinkedListAlgorithm,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK
    ):
        self.algorithm = algorithm
        self.forward_link = forward_link
        self.backward_link = backward_link

    def to_string(self, node, reverse=False, include_end=True):
        if not node:
            return "None" if include_end else ""
        string, link = "", self.backward_link if reverse else self.forward_link
        while self.algorithm.has_next(node):
            new_string = f"{self.algorithm.get_data(node)}"
            string = link + new_string + string if reverse else string + new_string + link
            node = self.algorithm.get_next(node)
        new_string = f"{self.algorithm.get_data(node)}"
        if include_end:
            return "None" + link + new_string + string if reverse else string + new_string + link + "None"
        else:
            return new_string + string if reverse else string + new_string

    def print(self, node, reverse=False, include_end=True):
        print(self.to_string(node, reverse, include_end))


class DoublyLinkedListPrinter:
    def __init__(self, algorithm: DoublyLinkedListAlgorithm,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        self.algorithm = algorithm
        self.forward_link = forward_link
        self.backward_link = backward_link
        self.bidirection_link = bidirection_link

    def to_string(self, node, include_end=True):
        if not node:
            return "None" if include_end else ""
        string, backward_node = "", self.algorithm.get_prev(node)
        while self.algorithm.has_next(node):
            string += f"{self.algorithm.get_data(node)}{self.bidirection_link}"
            node = self.algorithm.get_next(node)
        string += f"{self.algorithm.get_data(node)}{self.forward_link}None" if include_end else f"{self.algorithm.get_data(node)}"
        if not backward_node:
            return f"None{self.backward_link}{string}" if include_end else string
        node = backward_node
        while node:
            string = f"{self.algorithm.get_data(node)}{self.bidirection_link}" + string
            node = self.algorithm.get_prev(node)
        return f"None{self.backward_link}{string}" if include_end else string

    def print(self, node, include_end=True):
        print(self.to_string(node, include_end))



