from __future__ import annotations

from ezcode.list.const import DATA_NAME, NEXT_NAME, FORWARD_LINK, BACKWARD_LINK
from ezcode.list.algorithm import SinglyLinkedListAlgorithm
from ezcode.list.printer import SinglyLinkedListPrinter


class SinglyLinkedList(object):
    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.head = head
        self.algorithm = SinglyLinkedListAlgorithm(data_name, next_name)

    def add_to_head(self, data):
        new_node = self.algorithm.new_node(data=data)
        self.algorithm.set_next(node=new_node, next_node=self.head)
        self.head = new_node

    def peak_head(self):
        if not self.head:
            raise IndexError("Peak at an empty list")
        return self.algorithm.get_data(self.head)

    def pop_head(self):
        if not self.head:
            raise IndexError("Pop an empty list")
        node = self.head
        self.algorithm.set_next(node=self.head, next_node=self.algorithm.get_next(self.head))
        return node

    def calculate_size(self) -> int:
        size, node = 0, self.head
        while node:
            size, node = size + 1, self.algorithm.get_next(node)
        return size

    def to_string(self, reverse=False, forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK):
        printer = SinglyLinkedListPrinter(self.algorithm, forward_link, backward_link)
        printer.to_string(self.head, reverse)

    def print(self, reverse=False, forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK):
        print(self.to_string(reverse, forward_link, backward_link))

    def to_array(self):
        array, node = list(), self.head
        while node:
            array.append(self.algorithm.get_data(node))
            node = self.algorithm.get_next(node)
        return array

    def copy(self):
        if not self.head:
            return None
        other_head = self.algorithm.new_node(data=self.algorithm.get_data(self.head))
        other_node = other_head
        self_node = self.algorithm.get_next(self.head)
        while self_node:
            self.algorithm.set_next(node=other_node, next_node=self.algorithm.new_node(self.algorithm.get_data(self_node)))
            self_node = self.algorithm.get_next(self_node)
            other_node = self.algorithm.get_next(other_node)
        return SinglyLinkedList(other_head, self.algorithm.data_name, self.algorithm.next_name)

    def is_copied(self, other_list: SinglyLinkedList) -> bool:
        other_head = other_list.head
        if self.head:
            self_node, other_node = self.head, other_head
            while self_node:
                if self.algorithm.get_data(self_node) != self.algorithm.get_data(other_node):
                    return False
                self_node = self.algorithm.get_next(self_node)
                other_node = self.algorithm.get_next(other_node)
            return True
        else:
            return other_head == None

    def reverse(self):
        if self.head:
            previous_node, current_node, next_node = None, self.head, self.algorithm.get_next(self.head)
            while next_node:
                self.algorithm.set_next(node=current_node, next_node=previous_node)
                previous_node = current_node
                current_node = next_node
                next_node = self.algorithm.get_next(next_node)
            self.head = current_node

    def delete(self, data):
        previous_node, current_node = self.algorithm.new_node(next_node=self.head), self.head
        fake_head = previous_node
        while current_node:
            if data == self.node_data(current_node):
                self.algorithm.set_next(node=previous_node, next_node=self.algorithm.get_next(current_node))
            else:
                previous_node = current_node
            current_node = self.algorithm.get_next(current_node)
        self.head = self.algorithm.get_next(fake_head)

    def delete_nth_from_end(self, n: int):
        fake_head = self.algorithm.new_node(next_node=head)
        if n >= 1:
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
        size_delta = self.calculate_size() - other_list.calculate_size()
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
            fast_node = self.algorithm.get_next(self.algorithm.get_next(fast_node)) # 2 times faster
            slow_node = self.algorithm.get_next(slow_node)
            if fast_node == slow_node:
                slow_node = self.head
                while slow_node != fast_node:
                    fast_node = self.algorithm.get_next(fast_node) # same speed as slow
                    slow_node = self.algorithm.get_next(slow_node)
                return slow_node
        return None









