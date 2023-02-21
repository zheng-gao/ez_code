from typing import Callable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.List.LinkedListConstant import PREV_NAME, BIDIRECTION_LINK
from ezcode.List.LinkedListIterator import LinkedListIterator, DoublyLinkedListIterator


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
        string, is_first_node = "", True
        for n in LinkedListIterator(
            head=node, reverse=False, iterate_node=True,
            data_name=self.data_name, next_name=self.next_name,
        ):
            if is_first_node:
                string, is_first_node = self.node_to_string(n), False
            else:
                n_str = self.node_to_string(n)
                string = f"{string} {self.forward_link} {n_str}" if reverse else f"{n_str} {self.backward_link} {string}"
        if string:
            if mark_head:
                string = f"(H) {string}" if reverse else f"{string} (H)"
            if include_end:
                string = f"{string} {self.forward_link} None" if reverse else f"None {self.backward_link} {string}"
        else:
            if mark_head:
                string = "(H)"
            if include_end:
                string = f"{string + ' ' if string else ''}None" if reverse else f"None{' ' + string if string else ''}"
        return string

    def print(self, node, reverse=False, include_end=True, mark_head=True):
        print(self.to_string(node, reverse, include_end, mark_head))


class TailedLinkedListPrinter(LinkedListPrinter):
    def __init__(self,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    ):
        super().__init__(data_name, next_name, forward_link, backward_link, node_to_string)

    def to_string(self, node, reverse=False, include_end=True, mark_head=True, mark_tail=True):
        string, is_first_node = "", True
        for n in LinkedListIterator(
            head=node, reverse=False, iterate_node=True,
            data_name=self.data_name, next_name=self.next_name,
        ):
            if is_first_node:
                string, is_first_node = self.node_to_string(n), False
            else:
                n_str = self.node_to_string(n)
                string = f"{string} {self.forward_link} {n_str}" if reverse else f"{n_str} {self.backward_link} {string}"
        if string:
            if mark_head:
                string = f"(H) {string}" if reverse else f"{string} (H)"
            if mark_tail:
                string = f"{string} (T)" if reverse else f"(T) {string}"
            if include_end:
                string = f"{string} {self.forward_link} None" if reverse else f"None {self.backward_link} {string}"
        else:
            if mark_head and mark_tail:
                string = "(H,T)" if reverse else "(T,H)"
            elif mark_head:
                string = "(H)"
            elif mark_tail:
                string = "(T)"
            if include_end:
                string = f"{string + ' ' if string else ''}None" if reverse else f"None{' ' + string if string else ''}"
        return string if string else "None"

    def print(self, node, reverse=False, include_end=True, mark_head=True, mark_tail=True):
        print(self.to_string(node, reverse, include_end, mark_head, mark_tail))


class DoublyLinkedListPrinter(LinkedListPrinter):
    def __init__(self,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME, prev_name: str = PREV_NAME,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK,
        node_to_string: Callable = None
    ):
        super().__init__(data_name, next_name, forward_link, backward_link, node_to_string)
        self.prev_name = prev_name
        self.bidirection_link = bidirection_link

    def to_string(self, node, reverse=False, include_end=True, mark_head=True, mark_tail=True):
        string, is_first_node = "", True
        for n in DoublyLinkedListIterator(
            head=node, tail=node, reverse=False, iterate_node=True,
            data_name=self.data_name, next_name=self.next_name, prev_name=self.prev_name
        ):
            if is_first_node:
                string, is_first_node = self.node_to_string(n), False
            else:
                n_str = self.node_to_string(n)
                string = f"{string} {self.bidirection_link} {n_str}" if reverse else f"{n_str} {self.bidirection_link} {string}"
        if node is not None:
            node = node.__dict__[self.prev_name]
        is_first_node = string == ""
        for n in DoublyLinkedListIterator(
            head=node, tail=node, reverse=True, iterate_node=True,
            data_name=self.data_name, next_name=self.next_name, prev_name=self.prev_name
        ):
            if is_first_node:
                string, is_first_node = self.node_to_string(n), False
            else:
                n_str = self.node_to_string(n)
                string = f"{n_str} {self.bidirection_link} {string}" if reverse else f"{string} {self.bidirection_link} {n_str}"
        if string:
            if mark_head and mark_tail:
                string = f"(H) {string} (T)" if reverse else f"(T) {string} (H)"
            elif mark_head:
                string = f"(H) {string}" if reverse else f"{string} (H)"
            elif mark_tail:
                string = f"{string} (T)" if reverse else f"(T) {string}"
            if include_end:
                string = f"None {self.backward_link} {string} {self.forward_link} None"
        else:
            if mark_head and mark_tail:
                string = "(H,T)" if reverse else "(T,H)"
            elif mark_head:
                string = "(H)"
            elif mark_tail:
                string = "(T)"
            if include_end:
                string = f"None {string} None" if string else "None"
        return string if string else "None"

    def print(self, node, reverse=False, include_end=True, mark_head=True, mark_tail=True):
        print(self.to_string(node, reverse, include_end, mark_head, mark_tail))






