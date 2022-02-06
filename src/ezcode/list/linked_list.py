from __future__ import annotations

from ezcode.list.const import DATA_NAME, NEXT_NAME, PREV_NAME, FORWARD_LINK, BACKWARD_LINK, BIDIRECTION_LINK
from ezcode.list.algorithm import SinglyLinkedListAlgorithm, DoublyLinkedListAlgorithm
from ezcode.list.printer import SinglyLinkedListPrinter, DoublyLinkedListPrinter


class SinglyLinkedList(object):
    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME):
        self.head = head
        self.algorithm = SinglyLinkedListAlgorithm(data_name, next_name)
        self.size = self.calculate_size()

    def __len__(self):
        return self.size

    def __str__(self):
        return self.to_string()

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
        printer.to_string(self.head, reverse, include_end)

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
            raise IndexError("Peek head at an empty list")
        return self.algorithm.get_data(self.head)

    def pop_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Pop head from an empty list")
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

    def copy(self):
        if not self.head:
            return None
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

    def delete(self, data_set: set):
        """ O(N) """
        previous_node, current_node = self.algorithm.new_node(next_node=self.head), self.head
        fake_head, count = previous_node, 0
        while current_node:
            if self.node_data(current_node) in data_set:
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
            fake_head = self.algorithm.new_node(next_node=head)
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
            fast_node = self.algorithm.get_next(self.algorithm.get_next(fast_node)) # 2 times faster
            slow_node = self.algorithm.get_next(slow_node)
            if fast_node == slow_node:
                slow_node = self.head
                while slow_node != fast_node:
                    fast_node = self.algorithm.get_next(fast_node) # same speed as slow
                    slow_node = self.algorithm.get_next(slow_node)
                return slow_node
        return None


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

    def to_string(self, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        printer = DoublyLinkedListPrinter(self.algorithm, forward_link, backward_link, bidirection_link)
        printer.to_string(self.head, include_end)

    def print(self, include_end=True,
        forward_link: str = FORWARD_LINK, backward_link: str = BACKWARD_LINK, bidirection_link: str = BIDIRECTION_LINK
    ):
        print(self.to_string(include_end, forward_link, backward_link, bidirection_link))

    def add_to_head(self, data):
        """ O(1) """
        new_node = self.algorithm.new_node(data=data)
        self.add_node_to_head(new_node)

    def add_node_to_head(self, node):
        """ O(1) """
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
            raise IndexError("Peek head at an empty list")
        return self.algorithm.get_data(self.head)

    def peek_tail(self):
        """ O(1) """
        if not self.tail:
            raise IndexError("Peek tail at an empty list")
        return self.algorithm.get_data(self.tail)

    def pop_head(self):
        """ O(1) """
        if not self.head:
            raise IndexError("Pop head from an empty list")
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
            raise IndexError("Pop tail from an empty list")
        data = self.algorithm.get_data(self.tail)
        self.tail = self.algorithm.get_prev(self.tail)
        if self.tail:
            self.algorithm.set_next(node=self.tail, next_node=None)
        else:
            self.head = None
        self.size -= 1
        return data

    def detach_node(self, node):
        if node == self.head:
            self.pop_head()
        elif node == self.tail:
            self.pop_tail()
        else:
            prev_node = self.algorithm.get_prev(node)
            next_node = self.algorithm.get_next(node)
            self.algorithm.set_next(node=prev_node, next_node=next_node)
            self.algorithm.set_prev(node=next_node, prev_node=prev_node)
            self.size -= 1

    









