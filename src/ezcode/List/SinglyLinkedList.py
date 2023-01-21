from __future__ import annotations

from ezcode.List import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.List.LinkedListAlgorithm import SinglyLinkedListAlgorithm
from ezcode.List.LinkedListPrinter import SinglyLinkedListPrinter
from ezcode.Array.Utils import validate_index_range


class SinglyLinkedList(object):
    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.head = head
        self.algorithm = SinglyLinkedListAlgorithm(data_name, next_name)
        self.size = self.calculate_size()

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return self.to_string()

    def equal(self, other: SinglyLinkedList) -> bool:
        if not isinstance(other, type(self)):
            return False
        if self.head:
            self_node, other_node = self.head, other.head
            while self_node:
                if not other_node:
                    return False
                if self.algorithm.get_data(self_node) != self.algorithm.get_data(other_node):
                    return False
                self_node = self.algorithm.get_next(self_node)
                other_node = self.algorithm.get_next(other_node)
            return other_node is None
        else:
            return other.head is None

    def copy(self):
        if not self.head:
            return SinglyLinkedList(data_name=self.algorithm.data_name, next_name=self.algorithm.next_name)
        other_head = self.algorithm.new_node(data=self.algorithm.get_data(self.head))
        other_node = other_head
        self_node = self.algorithm.get_next(self.head)
        while self_node:
            self.algorithm.set_next(
                node=other_node,
                next_node=self.algorithm.new_node(self.algorithm.get_data(self_node))
            )
            self_node = self.algorithm.get_next(self_node)
            other_node = self.algorithm.get_next(other_node)
        return SinglyLinkedList(other_head, self.algorithm.data_name, self.algorithm.next_name)

    def calculate_size(self) -> int:
        """ O(N) """
        size, node = 0, self.head
        while node:
            size, node = size + 1, self.algorithm.get_next(node)
        return size

    def to_string(self, reverse=False, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK
    ):
        printer = SinglyLinkedListPrinter(self.algorithm, forward_link, backward_link)
        return printer.to_string(self.head, reverse, include_end)

    def print(self, reverse=False, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK
    ):
        print(self.to_string(reverse, include_end, forward_link, backward_link))

    def add_to_head(self, data):
        """ O(1) """
        new_node = self.algorithm.new_node(data=data, next_node=self.head)
        self.head = new_node
        self.size += 1

    def peek_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Peek head at an empty SinglyLinkedList")
        return self.algorithm.get_data(self.head)

    def pop_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Pop head from an empty SinglyLinkedList")
        data = self.algorithm.get_data(self.head)
        self.head = self.algorithm.get_next(self.head)
        self.size -= 1
        return data

    def to_array(self):
        array, node = list(), self.head
        while node:
            array.append(self.algorithm.get_data(node))
            node = self.algorithm.get_next(node)
        return array

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
        validate_index_range(start_index, end_index, 0, self.size - 1)
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

    def delete(self, data_set: set):
        """ O(N) """
        previous_node, current_node = self.algorithm.new_node(next_node=self.head), self.head
        fake_head, count = previous_node, 0
        while current_node:
            if self.algorithm.get_data(current_node) in data_set:
                self.algorithm.set_next(node=previous_node, next_node=self.algorithm.get_next(current_node))
                count += 1
            else:
                previous_node = current_node
            current_node = self.algorithm.get_next(current_node)
        self.head = self.algorithm.get_next(fake_head)
        self.size -= count

    def delete_nth_from_end(self, n: int = 1):
        """ O(N) """
        if n >= 1 and n <= self.size:
            fake_head = self.algorithm.new_node(next_node=self.head)
            fast_node, slow_node = self.head, fake_head
            for _ in range(n):  # move fast node n steps
                if not fast_node:
                    return
                fast_node = self.algorithm.get_next(fast_node)
            while fast_node:
                fast_node = self.algorithm.get_next(fast_node)
                slow_node = self.algorithm.get_next(slow_node)
            self.algorithm.set_next(node=slow_node, next_node=self.algorithm.get_next(slow_node, 2))
            self.algorithm.set_next(node=self.head, next_node=self.algorithm.get_next(fake_head))
            self.size -= 1
        else:
            raise IndexError(f"n = {n} is out of range [1, {self.size}]")

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

    def has_cycle(self):
        fast_node, slow_node = self.head, self.head
        while fast_node and self.algorithm.get_next(fast_node):
            fast_node = self.algorithm.get_next(self.algorithm.get_next(fast_node))
            slow_node = self.algorithm.get_next(slow_node)
            if fast_node == slow_node:
                return True
        return False

    def get_cycle_entrance(self):
        # https://en.wikipedia.org/wiki/Cycle_detection
        #   ┌─────── A ───────┐┌──── B ────┐
        #  n1 -> n2 -> ... -> n3 -> ... -> n4 <-- meeting point
        #                   ┌ ^            | ─┐   circle perimeter = C
        #                   │ |            v  │   B < C
        #                   │ n6 <- ... <- n5 │
        #                   └───── C - B ─────┘
        # When the fast meets the slow, the fast has walked N rounds in the circle, where N > 1
        # (A + B) * 2 = A + B + C * N, since the fast is 2 times faster than the slow
        # => A + B = C * N
        # => A = (C - B) + C * (N - 1)
        # C - B is the length from the meeting point (n4) to the entering point (n3)
        # so if one pointer start from head and another start from the meeting point at the same speed
        # they will meet at the entering point and the one in the circle will have walked (N - 1) rounds
        fast_node, slow_node = self.head, self.head
        while fast_node and self.algorithm.get_next(fast_node):
            fast_node = self.algorithm.get_next(self.algorithm.get_next(fast_node))  # 2 times faster
            slow_node = self.algorithm.get_next(slow_node)
            if fast_node == slow_node:
                slow_node = self.head
                while slow_node != fast_node:
                    fast_node = self.algorithm.get_next(fast_node)  # same speed as slow
                    slow_node = self.algorithm.get_next(slow_node)
                return slow_node
        return None


