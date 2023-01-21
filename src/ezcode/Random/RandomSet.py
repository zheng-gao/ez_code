from collections import defaultdict
from random import choice
from typing import Iterable


class RandomMultiSet:
    def __init__(self, init_data: Iterable = None):
        self.items = list()
        self.indices = defaultdict(set)  # {item: {index1, index2, ...}}
        if init_data is not None:
            for item in init_data:
                self.add(item)

    def __len__(self):
        return len(self.items)

    def __contains__(self, item) -> bool:
        """ O(1) """
        return item in self.indices

    def add(self, item):
        """ O(1) """
        self.indices[item].add(len(self.items))
        self.items.append(item)

    def remove(self, item):
        """ O(1) """
        if item in self.indices:
            index = self.indices[item].pop()
            if len(self.indices[item]) == 0:
                del self.indices[item]
            if index != len(self.items) - 1:
                last_index = len(self.items) - 1
                last_item = self.items[-1]
                self.items[index] = last_item
                self.indices[last_item].remove(last_index)
                self.indices[last_item].add(index)
            self.items.pop()
        else:
            raise KeyError(f"{item} not found")

    def random(self):
        """ O(1) """
        return choice(self.items)
