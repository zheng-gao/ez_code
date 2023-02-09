from typing import Callable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.List.LinkedListIterator import LinkedListIterator


class LinkedListPrinter:
    def __init__(self,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    ):
        self.data_name = data_name
        self.next_name = next_name
        self.forward_link = forward_link
        self.backward_link = backward_link
        self.node_to_string = (lambda node: str(node.__dict__[self.data_name])) if node_to_string is None else node_to_string

    def to_string(self, node, reverse=False, include_end=True, mark_head=True):
        string, is_first_node = "None", True
        for node in LinkedListIterator(
            head=node, reverse=(not reverse), iterate_node=True,
            data_name=self.data_name, next_name=self.next_name,
        ):
            if is_first_node:
                string, is_first_node = self.node_to_string(node), False
                if include_end:
                    string = f"{string} {self.forward_link} None" if reverse else f"None {self.backward_link} {string}"
            else:
                node_str = self.node_to_string(node)
                string = f"{node_str} {self.forward_link} {string}" if reverse else f"{string} {self.backward_link} {node_str}"
        return f"{'(H) ' if mark_head else ''}{string}" if reverse else f"{string}{' (H)' if mark_head else ''}"

    def print(self, node, reverse=False, include_end=True):
        print(self.to_string(node, reverse, include_end))
