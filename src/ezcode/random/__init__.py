from collections import defaultdict
from random import choice


class RandomMultiSet:
    def __init__(self):
        self.items = list()
        self.item_indices = defaultdict(set)

    def __contains__(self, item) -> bool:
        return item in self.item_indices

    def add(self, item):
        """ O(1) """
        self.item_indices[item].add(len(self.items))
        self.items.append(item)

    def remove(self, item):
        """ O(1) """
        if item in self.item_indices:
            index = self.item_indices[item].pop()
            if len(self.item_indices[item]) == 0:
                del self.item_indices[item]
            if index != len(self.items) - 1:
                last_index, last_item = len(self.items) - 1, self.items[-1]
                self.items[index] = last_item
                self.item_indices[last_item].remove(last_index)
                self.item_indices[last_item].add(index)
            self.items.pop()
        else:
            raise KeyError(f"{item} not found")

    def random(self):
        """ O(1) """
        return choice(self.items)
