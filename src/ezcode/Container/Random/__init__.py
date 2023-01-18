from collections import defaultdict
from random import choice, random

from ezcode.Container.Tree.SegmentTree import SegmentTree


class RandomMultiSet:
    def __init__(self, data=None):
        self.items = list()
        self.indices = defaultdict(set)  # {item: {index1, index2, ...}}
        if data is not None:
            for item in data:
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


class RandomDict:
    def __init__(self, data: dict = None):
        self.key_value_dict = dict()  # {key: value}
        if data is not None:
            for key, value in data.items():
                self[key] = value

    def __len__(self):
        return len(self.key_value_dict)

    def __contains__(self, key) -> bool:
        """ O(1) """
        return key in self.key_value_dict

    def __getitem__(self, key):
        """ O(1) """
        if key not in self.key_value_dict:
            raise KeyError(f"{key} not found")
        return self.key_value_dict[key]

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def items(self):
        return self.key_value_dict.items()

    def keys(self):
        return self.key_value_dict.keys()

    def values(self):
        return self.key_value_dict.values()

    def random_value(self):
        pass


class RandomKeyValueDict(RandomDict):
    def __init__(self, data: dict = None):
        self.key_list = list()            # [key]
        self.key_index_dict = dict()  # {key: index of key_list}
        super().__init__(data=data)

    def __setitem__(self, key, value):
        """ O(1) """
        if key not in self.key_value_dict:
            self.key_index_dict[key] = len(self.key_list)
            self.key_list.append(key)
        self.key_value_dict[key] = value

    def __delitem__(self, key):
        """ O(1) """
        if key not in self.key_value_dict:
            raise KeyError(f"{key} not found")
        index = self.key_index_dict[key]
        last_key = self.key_list[-1]
        self.key_list[index] = last_key
        self.key_index_dict[last_key] = index
        self.key_list.pop()
        del self.key_index_dict[key]
        del self.key_value_dict[key]

    def random_key(self):
        """ O(1), probability = 1 / total number of keys """
        return choice(self.key_list)

    def random_value(self):
        """ O(1), probability = value occurences / total number of values """
        return self.key_value_dict[self.random_key()]


class RandomUniqueValueDict(RandomDict):
    def __init__(self, data: dict = None):
        self.unique_value_list = list()  # [value]
        self.value_index_dict = dict()   # {value: index of unique_value_list}
        self.value_counter = dict()      # {value: count of duplicates}
        super().__init__(data=data)

    def __setitem__(self, key, value):
        """ O(1) """
        if value not in self.value_index_dict:
            self.value_index_dict[value] = len(self.unique_value_list)
            self.unique_value_list.append(value)
            self.value_counter[value] = 1
        else:
            self.value_counter[value] += 1
        self.key_value_dict[key] = value

    def __delitem__(self, key):
        """ O(1) """
        if key not in self.key_value_dict:
            raise KeyError(f"{key} not found")
        value = self.key_value_dict[key]
        if self.value_counter[value] > 1:
            self.value_counter[value] -= 1
        else:
            index = self.value_index_dict[value]
            last_unique_value = self.unique_value_list[-1]
            self.unique_value_list[index] = last_unique_value
            self.value_index_dict[last_unique_value] = index
            self.unique_value_list.pop()
            del self.value_index_dict[value]
            del self.value_counter[value]
        del self.key_value_dict[key]

    def random_value(self):
        """ O(1), probability = 1 / total number of unique values """
        return choice(self.unique_value_list)


class ArrayBasedRandomWeightedIndex:
    def __init__(self, weights: list):
        """ build cumulative_sum: O(N) """
        self.weights = weights.copy()  # Save the weights only when update is required
        self.sum = 0
        self.cumulative_sum = list()
        for weight in weights:
            self.sum += weight
            self.cumulative_sum.append(self.sum)

    def update(self, index: int, weight):
        """ Time: O(N) """
        weight_diff = weight - self.weights[index]
        self.weights[index] = weight
        self.sum += weight_diff
        for i in range(index, len(self.cumulative_sum)):
            self.cumulative_sum[i] += weight_diff

    def random_index(self) -> int:
        """ Time: O(logN) """
        r = random() * self.sum  # random() -> [0, 1)
        start, end = 0, len(self.cumulative_sum) - 1
        while start < end:
            mid = start + (end - start) // 2
            if r < self.cumulative_sum[mid]:
                end = mid
            else:
                start = mid + 1
        return start


class TreeBasedRandomWeightedIndex:
    def __init__(self, weights: list):
        """ build tree time: O(N) """
        self.segment_tree = SegmentTree(data_list=weights, merge=lambda x, y: x + y)

    def update(self, index: int, weight):
        """ Time: O(logN) """
        self.segment_tree.update(index, weight)

    def random_index(self):
        """ Time: O(logN) """
        node = self.segment_tree.root
        while node.left is not None:  # Segment Tree is Complete
            if node.right is None:
                node = node.left
            else:  # [0.0, node.data)
                node = node.left if random() * node.data < node.left.data else node.right
        return node.start





