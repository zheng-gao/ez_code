from random import choice


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


