from __future__ import annotations
from collections.abc import MutableMapping
from enum import Enum

from ezcode.List.DoublyLinkedList import DoublyLinkedList
from ezcode.List.LinkedListIterator import DoublyLinkedListIterator


class LRUCacheIterator:
    Mode = Enum("Mode", ["KEY", "VALUE", "ITEM"])

    def __init__(self, doubly_linked_list, reverse=False, mode=Mode.KEY):
        self.mode = mode
        self.iterator = DoublyLinkedListIterator(
            head=doubly_linked_list.head,
            tail=doubly_linked_list.tail,
            data_name=doubly_linked_list.data_name,
            next_name=doubly_linked_list.next_name,
            prev_name=doubly_linked_list.prev_name,
            reverse=reverse, iterate_node=False
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self.mode == LRUCacheIterator.Mode.KEY:
            return next(self.iterator).key
        elif self.mode == LRUCacheIterator.Mode.VALUE:
            return next(self.iterator).value
        else:
            entry = next(self.iterator)
            return entry.key, entry.value


class LRUCache(MutableMapping):
    class Entry:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.cache = dict()             # {key: list node}
        self.list = DoublyLinkedList()  # node.data = Entry(key, value)

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key) -> bool:
        return key in self.cache

    def __iter__(self):
        """ The most recent first """
        return LRUCacheIterator(doubly_linked_list=self.list, reverse=False, mode=LRUCacheIterator.Mode.KEY)

    def __reversed__(self):
        """ The most recent last """
        return LRUCacheIterator(doubly_linked_list=self.list, reverse=True, mode=LRUCacheIterator.Mode.KEY)

    def __getitem__(self, key):
        if key not in self.cache:
            raise KeyError(f"Not Found: {key}")
        node = self.cache[key]
        self.list.remove_node(node)
        self.list.append_node(node)
        return self.list.get_data(node).value  # node.data = Entry(key, value)

    def __delitem__(self, key):
        if key not in self.cache:
            raise KeyError(f"Not Found: {key}")
        self.list.remove_node(self.cache[key])
        del self.cache[key]

    def __setitem__(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            self.list.set_data(node=node, data=self.Entry(key, value))
            self.list.remove_node(node)
        else:
            if len(self) == self.capacity:
                del self.cache[self.list.get_data(self.list.tail).key]
                self.list.remove_node(self.list.tail)
            node = self.list.new_node(data=self.Entry(key, value))
            self.cache[key] = node
        self.list.append_node(node)

    def clear(self):
        self.cache.clear()
        self.list.clear()

    def keys(self, reverse=False):  # default: most recent first, reverse: most recent last
        yield from LRUCacheIterator(doubly_linked_list=self.list, reverse=reverse, mode=LRUCacheIterator.Mode.KEY)

    def values(self, reverse=False):  # default: most recent first, reverse: most recent last
        yield from LRUCacheIterator(doubly_linked_list=self.list, reverse=reverse, mode=LRUCacheIterator.Mode.VALUE)

    def items(self, reverse=False):  # default: most recent first, reverse: most recent last
        yield from LRUCacheIterator(doubly_linked_list=self.list, reverse=reverse, mode=LRUCacheIterator.Mode.ITEM)

    def pop(self, key):
        if key not in self.cache:
            raise KeyError(f"Not Found: {key}")
        node = self.cache[key]
        self.list.remove_node(node)
        del self.cache[key]
        return self.list.get_data(node).value

    def popitem(self, reverse=False):  # default: most recent, reverse: least recent
        if len(self.cache) == 0:
            raise KeyError("Pop from empty cache")
        node = self.list.tail if reverse else self.list.head
        del self.cache[self.list.get_data(node).key]
        self.list.remove_node(node)
        data = self.list.get_data(node)
        return data.key, data.value





