class StackOnPartialArray:
    def __init__(self, array: list, start: int, end: int):
        self.array = array
        self.start = start
        self.end = end
        self.size = 0
        self.head = start - 1

    def __len__(self):
        return self.size

    def push(self, data):
        if self.size == self.end - self.start + 1:
            raise IndexError("Push to a full stack")
        self.head += 1
        self.array[self.head] = data
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("Pop from an empty queue")
        data = self.array[self.head]
        self.head -= 1
        self.size -= 1
        return data

    def top(self, k: int = 1, always_return_list: bool = False):
        if k <= 0:
            raise ValueError(f"Cannot take non-positive value: {k}")
        if len(self) < k:
            raise ValueError(f"Not enough items, size: {len(self)}, k: {k}")
        if k == 1:
            return [self.array[self.head]] if always_return_list else self.array[self.head]
        else:
            head, output = self.head, list()
            for _ in range(k):
                output.append(self.array[head])
                head -= 1
            return output
