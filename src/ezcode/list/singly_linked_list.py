from __future__ import annotations

from ezcode.list.const import DATA_NAME, NEXT_NAME
from ezcode.list.algorithm import SinglyLinkedListAlgorithm


class SinglyLinkedList(object):

    class FakeNode(object):
        def __init__(self):
           pass

    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.head = head
        self.data_name = data_name
        self.next_name = next_name
        self.algorithm = SinglyLinkedListAlgorithm(data_name, next_name)
        self.size = self.calculate_size()

    def calculate_size(self) -> int:
        size, node = 0, self.head
        while node:
            node = self.get_next_node(node)
            size += 1
        return size

    def new_node(self, data=None, next_node=None):
        node = self.FakeNode()
        node.__dict__ = {self.data_name: data, self.next_name: next_node}
        return node

    def get_next_node(self, node, steps: int = 1):
        next_node = node
        for _ in range(steps):
            next_node = next_node.__dict__[self.next_name]
        return next_node

    def set_next_node(self, node, next_node=None):
        node.__dict__[self.next_name] = next_node

    def get_node_data(self, node):
        return node.__dict__[self.data_name]

    def print(self, reverse=False):
        if reverse:
            self.algorithm.reverse_print(self.head, self.head)
        else:
            node = self.head
            while node and self.get_next_node(node):
                print(f"{self.get_node_data(node)} -> ", end="")
                node = self.get_next_node(node)
            if node:
                print(f"{self.get_node_data(node)} -> ", end="")
            print("None")

    def to_array(self):
        array, node = list(), self.head
        while node:
            array.append(self.get_node_data(node))
            node = self.get_next_node(node)
        return array

    def copy(self):
        if not self.head:
            return None
        other_head = self.new_node(data=self.get_node_data(self.head))
        other_node = other_head
        self_node = self.get_next_node(self.head)
        while self_node:
            self.set_next_node(node=other_node, next_node=self.new_node(self.get_node_data(self_node)))
            self_node = self.get_next_node(self_node)
            other_node = self.get_next_node(other_node)
        return SinglyLinkedList(other_head, self.data_name, self.next_name)

    def is_copied(self, other_list: SinglyLinkedList) -> bool:
        other_head = other_list.head
        if self.head:
            self_node, other_node = self.head, other_head
            while self_node:
                if self.get_node_data(self_node) != self.get_node_data(other_node):
                    return False
                self_node = self.get_next_node(self_node)
                other_node = self.get_next_node(other_node)
            return True
        else:
            return other_head == None

    def reverse(self):
        if self.head:
            # self.head = self.algorithm.reverse(self.head, self.get_next_node(self.head))
            previous_node, current_node, next_node = None, self.head, self.get_next_node(self.head)
            while next_node:
                self.set_next_node(node=current_node, next_node=previous_node)
                previous_node = current_node
                current_node = next_node
                next_node = self.get_next_node(next_node)
            self.head = current_node

    def delete(self, data):
        previous_node, current_node = self.new_node(next_node=self.head), self.head
        fake_head = previous_node
        while current_node:
            if data == self.node_data(current_node):
                self.set_next_node(node=previous_node, next_node=self.get_next_node(current_node))
            else:
                previous_node = current_node
            current_node = self.get_next_node(current_node)
        self.head = self.get_next_node(fake_head)

    def delete_nth_from_end(self, n: int):
        fake_head = self.new_node(next_node=head)
        if n >= 1:
            fast_node, slow_node = self.head, fake_head
            for _ in range(n):  # move fast node n steps
                if not fast_node:
                    return
                fast_node = self.get_next_node(fast_node)
            while fast_node:
                fast_node = self.get_next_node(fast_node)
                slow_node = self.get_next_node(slow_node)
            self.set_next_node(node=slow_node, next_node=self.get_next_node(slow_node, 2))
        self.set_next_node(node=self.head, next_node=self.get_next_node(fake_head))

    def swap_pairs(self):
        if self.head and self.get_next_node(self.head):
            # We need 3 nodes to swap a pair of nodes (second, third)
            # first second third
            #   |      |     |
            #  fake    n1 -> n2 -> n3 -> n4 -> ...
            fake_head = self.new_node()
            first, second, third = fake_head, self.head, self.get_next_node(self.head)
            while third:
                self.set_next_node(node=first, next_node=third)
                self.set_next_node(node=second, next_node=self.get_next_node(third))
                self.set_next_node(node=third, next_node=second)
                # first second third
                #   |      |     |
                #  fake    n1 <- n2    n3 -> n4 -> ...  
                #   |------|-----^     ^ 
                #          |-----------|
                third = self.get_next_node(second)
                # first       second third
                #   |           |     |
                # fake -> n2 -> n1 -> n3 -> n4 -> ...
                if not third or not self.get_next_node(third):
                    break
                first, second, third = second, third, self.get_next_node(third)
                #             first second third
                #               |     |     |
                # fake -> n2 -> n1 -> n3 -> n4 -> ...
            self.head = self.get_next_node(fake_head)

    def get_intersection_head(self, other_list: SinglyLinkedList):
        size_delta = self.size - other_list.size
        long_list_node, short_list_node = (self.head, other_list.head) if size_delta > 0 else (other_list.head, self.head)
        long_list_node = self.get_next_node(node=long_list_node, steps=abs(size_delta))
        while short_list_node and short_list_node != long_list_node:
            short_list_node = self.get_next_node(short_list_node)
            long_list_node = self.get_next_node(long_list_node)
        return short_list_node

    def has_cycle(self):
        fast_node, slow_node = self.head, self.head
        while fast_node and self.get_next_node(fast_node):
            fast_node = self.get_next_node(self.get_next_node(fast_node))
            slow_node = self.get_next_node(slow_node)
            if fast_node == slow_node:
                return True
        return False

    def get_cycle_entrance(self):
        #   ┌─────── A ───────┐┌──── B ────┐
        #  n1 -> n2 -> ... -> n3 -> ... -> n4 <- meeting point
        #                   ┌ ^            | ─┐   circle perimeter = C
        #                   │ |            v  │
        #                   │ n6 <- ... <- n5 │
        #                   └───── C - B ─────┘
        # When the fast meets the slow, the fast has walked N rounds in the circle, where N > 1 
        # (A + B) * 2 = A + B + C * N, since the fast is 2 times faster than the slow 
        # A + B = C * N, where B < C
        # A = (C - B) + C * (N - 1)
        # C - B is the length from the meeting point (n4) to the entering point (n3)
        # so if one pointer start from head and another start from the meeting point at the same speed
        # they will meet at the entering point and the one in the circle will walk n - 1 rounds
        fast_node, slow_node = self.head, self.head
        while fast_node and self.get_next_node(fast_node):
            fast_node = self.get_next_node(self.get_next_node(fast_node)) # 2 times faster
            slow_node = self.get_next_node(slow_node)
            if fast_node == slow_node:
                slow_node = self.head
                while slow_node != fast_node:
                    fast_node = self.get_next_node(fast_node) # same speed as slow
                    slow_node = self.get_next_node(slow_node)
                return slow_node
        return None









