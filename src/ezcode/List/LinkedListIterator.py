from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, PREV_NAME


class LinkedListIterator:
    def __init__(self,
        head=None,
        data_name: str = DATA_NAME,
        next_name: str = NEXT_NAME,
        reverse=False,
        iterate_node=False
    ):
        self.head = head
        self.iterate_node = iterate_node
        self.data_name = data_name
        self.next_name = next_name
        self.choose_generator(reverse)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterate_node:
            return next(self.generator)
        return next(self.generator).__dict__[self.data_name]

    def choose_generator(self, reverse):
        self.generator = self.backward(self.head) if reverse else self.forward(self.head)

    def forward(self, node):
        """ 0 <- 1 <- 2 <- head """
        if node is not None:
            yield node
            yield from self.forward(node.__dict__[self.next_name])

    def backward(self, node):
        """ 0 -> 1 -> 2 -> head """
        if node is not None:
            yield from self.backward(node.__dict__[self.next_name])
            yield node


class DoublyLinkedListIterator(LinkedListIterator):
    def __init__(self,
        head=None,
        tail=None,
        data_name: str = DATA_NAME,
        next_name: str = NEXT_NAME,
        prev_name: str = PREV_NAME,
        reverse=False,
        iterate_node=False
    ):
        self.tail = tail
        self.prev_name = prev_name
        super().__init__(head, data_name, next_name, reverse, iterate_node)

    def choose_generator(self, reverse):
        self.generator = self.backward(self.tail) if reverse else self.forward(self.head)

    def backward(self, node):
        """ tail -> 0 -> 1 -> 2 -> head """
        if node is not None:
            yield node
            yield from self.backward(node.__dict__[self.prev_name])




