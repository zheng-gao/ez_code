from collections import defaultdict
from random import choice


class RandomMultiSet:
    def __init__(self):
        self.items = list()
        self.indices = defaultdict(set)  # {item: {index1, index2, ...}}

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
                last_index, last_item = len(self.items) - 1, self.items[-1]
                self.items[index] = last_item
                self.indices[last_item].remove(last_index)
                self.indices[last_item].add(index)
            self.items.pop()
        else:
            raise KeyError(f"{item} not found")

    def random(self):
        """ O(1) """
        return choice(self.items)


class RandomDictionary:
    def __init__(self):
        self.keys = list()  # [key]
        self.key_index_dict = dict()  # {key: key_index}
        self.key_value_dict = dict()  # {key: value}

    def __contains__(self, key) -> bool:
        """ O(1) """
        return key in self.key_index_dict

    def __getitem__(self, key):
        """ O(1) """
        if key not in self.key_index_dict:
            raise KeyError(f"{key} not found")
        return self.key_value_dict[key]

    def __setitem__(self, key, value):
        """ O(1) """
        if key not in self.key_index_dict:
            self.key_index_dict[key] = len(self.keys)
            self.keys.append(key)
        self.key_value_dict[key] = value

    def __delitem__(self, key):
        """ O(1) """
        if key not in self.key_index_dict:
            raise KeyError(f"{key} not found")
        index, last_key = self.key_index_dict[key], self.keys[-1]
        self.keys[index] = last_key
        self.key_index_dict[last_key] = index
        self.keys.pop()
        del self.key_index_dict[key]
        del self.key_value_dict[key]

    def random_key(self):
        """ O(1), probability = 1 / total number of keys """
        return choice(self.keys)

    def random_value(self):
        """ O(1), probability = value occurences / total number of values """
        return self.key_value_dict[self.random_key()]





