from collections.abc import MutableSequence, Container
from typing import Iterable, Callable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.List.LinkedListIterator import LinkedListIterator
from ezcode.List.LinkedListPrinter import LinkedListPrinter


class LinkedList(MutableSequence):
    class LinkedListNode:
        def __init__(self):
            pass

        def match(self, other) -> bool:
            if any(key not in self.__dict__.keys() for key in other.__dict__.keys()):
                return False
            if any(key not in other.__dict__.keys() for key in self.__dict__.keys()):
                return False
            return True

    def __init__(self,
        init_data: Iterable = None, head=None, head_copy=None,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME
    ):
        self.head, self.size = head, 0
        self.data_name = data_name
        self.next_name = next_name
        if head is not None:  # Any change on this list will affect the original list on the head
            self._size()       # Recalculate the size, Time: O(N)
        elif head_copy is not None:
            self.copy_from(head_copy)
        if init_data is not None:
            for data in init_data:
                self.append(data)

    def _size(self):  # recalculate the size
        """ Time: O(N) """
        self.size = 0
        for _ in reversed(self):
            self.size += 1
        return self.size

    def new_node(self, data=None, next_node=None):
        node = self.LinkedListNode()
        node.__dict__ = {self.data_name: data, self.next_name: next_node}
        return node

    def node_to_string(self, node) -> str:
        return str(self.get_data(node))

    def get_data(self, node):
        return node.__dict__[self.data_name]

    def set_data(self, node, data):
        node.__dict__[self.data_name] = data

    def get_next(self, node, steps: int = 1):
        for _ in range(steps):
            if node is None:
                return None
            node = node.__dict__[self.next_name]
        return node

    def has_next(self, node, steps: int = 1) -> bool:
        if not node:
            return False
        for _ in range(steps):
            node = node.__dict__[self.next_name]
            if not node:
                return False
        return True

    def set_next(self, node, next_node=None):
        node.__dict__[self.next_name] = next_node

    def __iter__(self):
        """ from index 0 (last element) to head """
        return LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=True, iterate_node=False
        )

    def __reversed__(self):
        """ from index -1 (first/head element) to end """
        return LinkedListIterator(
            head=self.head, data_name=self.data_name, next_name=self.next_name,
            reverse=False, iterate_node=False
        )

    def __contains__(self, data):
        return any(d == data for d in reversed(self))

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int):
        return self.get_data(self.get_node(index))

    def __setitem__(self, index: int, data):
        self.set_data(node=self.get_node(index), data=data)

    def __delitem__(self, index: int):
        index = self.regularize_index(index)  # recalculate the index from head
        if index == 0:
            self.head = self.get_next(self.head)
        else:
            predecessor = self.get_next(node=self.head, steps=index - 1)
            self.set_next(node=predecessor, next_node=self.get_next(predecessor, steps=2))
        self.size -= 1

    def __add__(self, other: Iterable):
        new_list = self.copy()
        new_list.extend(other)
        return new_list

    def __iadd__(self, other: Iterable):
        self.extend(other)

    def __str__(self) -> str:
        return self.to_string()

    def print(self, reverse: bool = False, include_end: bool = True, mark_head: bool = True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    ):
        print(
            self.to_string(
                reverse=reverse, include_end=include_end, mark_head=mark_head,
                forward_link=forward_link, backward_link=backward_link,
                node_to_string=node_to_string
            )
        )

    def to_string(self,
        reverse: bool = False, include_end: bool = True, mark_head: bool = True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK,
        node_to_string: Callable = None
    ):
        return LinkedListPrinter(
            data_name=self.data_name, next_name=self.next_name,
            forward_link=forward_link, backward_link=backward_link,
            node_to_string=self.node_to_string if node_to_string is None else node_to_string
        ).to_string(node=self.head, reverse=reverse, include_end=include_end, mark_head=mark_head)

    def regularize_index(self, index: int, auto_fit: bool = False):
        """ recalculate index from head """
        if index > self.size - 1 or index < -self.size:
            if auto_fit:
                return 0 if self.size == 0 or index > 0 else (self.size - 1)
            raise IndexError(f"list index {index} out of range")
        return (self.size - 1 - index) if index >= 0 else (-1 - index)

    def get_node(self, index: int):
        return self.get_next(node=self.head, steps=self.regularize_index(index))

    def clear(self):
        self.head, self.size = None, 0

    def count(self, data):
        occurrences = 0
        for d in reversed(self):
            if data == d:
                occurrences += 1
        return occurrences

    def copy(self):
        list_copy = self.__class__()
        list_copy.copy_from(self)
        return list_copy

    def copy_from_node(self, node):
        if node is None:
            self.clear()
        else:
            if not (self.head is None and self.new_node().match(node)) and not (self.head is not None and self.head.match(node)):
                raise ValueError(f"Invalid node with attributes: {list(node.__dict__.keys())}")
            node_copy = self.new_node(data=self.get_data(node))
            self.head, self.size = node_copy, 1
            while self.get_next(node) is not None:
                node = self.get_next(node)
                next_node_copy = self.new_node(data=self.get_data(node))
                self.set_next(node=node_copy, next_node=next_node_copy)
                node_copy = next_node_copy
                self.size += 1

    def copy_from(self, other):
        if isinstance(other, self.__class__):
            self.data_name = other.data_name
            self.next_name = other.next_name
            self.copy_from_node(other.head)

    def extend(self, other: Iterable):
        for data in other:
            self.append(data)

    def append(self, data):
        self.head = self.new_node(data=data, next_node=self.head)
        self.size += 1

    def insert(self, index: int, data):
        index = self.regularize_index(index, auto_fit=True)
        if index == 0:
            self.append(data)
        else:
            node = self.get_next(node=self.head, steps=index)
            self.set_next(node=node, next_node=self.new_node(data=data, next_node=self.get_next(node)))
            self.size += 1

    def remove_all(self, data):
        is_data_container = isinstance(data, Container)
        predecessor, node = None, self.head
        while node is not None:
            next_node = self.get_next(node)
            node_data = self.get_data(node)
            if (is_data_container and node_data in data) or (not is_data_container and node_data == data):
                if node == self.head:
                    self.head = next_node
                else:
                    self.set_next(node=predecessor, next_node=next_node)
                self.size -= 1
            else:
                predecessor = node
            node = next_node

    def reverse(self):
        predecessor, node = None, self.head
        while node is not None:
            successor = self.get_next(node)
            self.set_next(node=node, next_node=predecessor)
            predecessor, node = node, successor
        self.head = predecessor

    def pop(self):
        if len(self) == 0:
            raise KeyError("Pop from empty list")
        data = self[-1]
        del self[-1]
        return data

    def equal(self, other) -> bool:
        """ This method should be overridden by the subclass if the subclass node has different attributes """
        if type(other) != self.__class__:
            return False
        if len(self) != len(other):
            return False
        for self_data, other_data in zip(iter(self), iter(other)):
            if self_data != other_data:
                return False
        return True

    def has_cycle(self, node):
        fast_node = slow_node = node
        while fast_node and self.get_next(fast_node):
            fast_node, slow_node = self.get_next(fast_node, steps=2), self.get_next(slow_node)
            if fast_node == slow_node:
                return True
        return False

    def get_cycle_entrance(self, node):
        """
        https://en.wikipedia.org/wiki/Cycle_detection
          ┌─────── A ───────┐┌──── B ────┐
         n1 -> n2 -> ... -> n3 -> ... -> n4 <-- meeting point
                          ┌ ^            | ─┐   circle perimeter = C
                          │ |            v  │   B < C
                          │ n6 <- ... <- n5 │
                          └───── C - B ─────┘
        When the fast meets the slow, the fast has walked N rounds in the circle, where N > 1
        (A + B) * 2 = A + B + C * N, since the fast is 2 times faster than the slow
        => A + B = C * N
        => A = (C - B) + C * (N - 1)
        C - B is the length from the meeting point (n4) to the entering point (n3)
        so if one pointer start from head and another start from the meeting point at the same speed
        they will meet at the entering point and the one in the circle will have walked (N - 1) rounds
        """
        fast_node = slow_node = node
        while fast_node and self.get_next(fast_node):
            fast_node, slow_node = self.get_next(fast_node, steps=2), self.get_next(slow_node)
            if fast_node == slow_node:
                slow_node = node
                while slow_node != fast_node:
                    fast_node, slow_node = self.get_next(fast_node), self.get_next(slow_node)  # same speed
                return slow_node
        return None


"""
    To Do
    def reverse(self, start_index: int = None, end_index: int = None):
        if start_index is None and end_index is None:
            if self.head:
                previous_node, current_node, next_node = None, self.head, self.algorithm.get_next(self.head)
                while next_node:
                    self.algorithm.set_next(node=current_node, next_node=previous_node)
                    previous_node = current_node
                    current_node = next_node
                    next_node = self.algorithm.get_next(next_node)
                self.algorithm.set_next(node=current_node, next_node=previous_node)
                self.head = current_node
        elif start_index is not None and end_index is not None:
            self._reverse_sublist(start_index, end_index)
        elif start_index is not None:
            self._reverse_sublist(start_index, self.size - 1)
        else:
            self._reverse_sublist(0, end_index)

    def _reverse_sublist(self, start_index: int, end_index: int):
        validate_index_interval(start_index, end_index, 0, self.size - 1)
        if not self.head or start_index == end_index:
            return
        start_node_prev, start_node, current_node, index = None, None, self.head, 0
        while current_node:
            if start_node is None and index == start_index:
                start_node = current_node
                index += 1
                break
            start_node_prev = current_node
            current_node = self.algorithm.get_next(current_node)
            index += 1
        previous_node, current_node, next_node = None, start_node, self.algorithm.get_next(start_node)
        while next_node is not None and index <= end_index:  # the tail is end_node.next
            self.algorithm.set_next(current_node, previous_node)
            previous_node = current_node
            current_node = next_node
            next_node = self.algorithm.get_next(next_node)
            index += 1
        self.algorithm.set_next(current_node, previous_node)
        self.algorithm.set_next(start_node, next_node)
        if start_node_prev is None:
            self.head = current_node
        else:
            self.algorithm.set_next(start_node_prev, current_node)


    def swap_pairs_of_nodes(self):
        if self.head and self.algorithm.get_next(self.head):
            # We need 3 nodes to swap a pair of nodes (second, third)
            # first second third
            #   |      |     |
            #  fake    n1 -> n2 -> n3 -> n4 -> ...
            fake_head = self.algorithm.new_node()
            first, second, third = fake_head, self.head, self.algorithm.get_next(self.head)
            while third:
                self.algorithm.set_next(node=first, next_node=third)
                self.algorithm.set_next(node=second, next_node=self.algorithm.get_next(third))
                self.algorithm.set_next(node=third, next_node=second)
                # first second third
                #   |      |     |
                #  fake    n1 <- n2    n3 -> n4 -> ...
                #   |------|-----^     ^
                #          |-----------|
                third = self.algorithm.get_next(second)
                # first       second third
                #   |           |     |
                # fake -> n2 -> n1 -> n3 -> n4 -> ...
                if not third or not self.algorithm.get_next(third):
                    break
                first, second, third = second, third, self.algorithm.get_next(third)
                #             first second third
                #               |     |     |
                # fake -> n2 -> n1 -> n3 -> n4 -> ...
            self.head = self.algorithm.get_next(fake_head)

    def get_intersection_head(self, other_list: SinglyLinkedList):
        size_delta = self.size - other_list.size
        long_list_node, short_list_node = (self.head, other_list.head) if size_delta > 0 else (other_list.head, self.head)
        long_list_node = self.algorithm.get_next(node=long_list_node, steps=abs(size_delta))
        while short_list_node and short_list_node != long_list_node:
            short_list_node = self.algorithm.get_next(short_list_node)
            long_list_node = self.algorithm.get_next(long_list_node)
        return short_list_node



"""






