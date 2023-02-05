from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME


class LinkedListIterator:
    def __init__(self, head=None, data_name: str = DATA_NAME, next_name: str = NEXT_NAME, reverse=False, iterate_node=False):
        self.iterate_node = iterate_node
        self.data_name = data_name
        self.next_name = next_name
        if reverse:
            self.generator = self._backward(head)
        else:
            self.generator = self._forward(head)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterate_node:
            return next(self.generator)
        return next(self.generator).__dict__[self.data_name]

    def _forward(self, node):
        """ 0 <- 1 <- 2 <- head """
        if node is not None:
            yield node
            yield from self._forward(node.__dict__[self.next_name])

    def _backward(self, node):
        """ 0 -> 1 -> 2 -> head """
        if node is not None:
            yield from self._backward(node.__dict__[self.next_name])
            yield node
