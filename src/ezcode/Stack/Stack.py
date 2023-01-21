from ezcode.List.SinglyLinkedList import SinglyLinkedList


class Stack:
    def __init__(self):
        self.singly_linked_list = SinglyLinkedList()

    def __len__(self):
        return len(self.singly_linked_list)

    def __str__(self):
        return self.singly_linked_list.to_string(reverse=True)

    def print(self):
        print(self)

    def push(self, data):
        self.singly_linked_list.add_to_head(data)

    def top(self, k: int = 1, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.singly_linked_list.peek_head()] if always_return_list else self.singly_linked_list.peek_head()
        else:
            node, output = self.singly_linked_list.head, list()
            for _ in range(k):
                output.append(self.singly_linked_list.algorithm.get_data(node))
                node = self.singly_linked_list.algorithm.get_next(node)
            return output

    def pop(self):
        if len(self) == 0:
            raise IndexError("Pop from an empty stack")
        return self.singly_linked_list.pop_head()
