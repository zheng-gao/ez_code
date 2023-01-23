from ezcode.List.DoublyLinkedList import DoublyLinkedList


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = dict()  # value = Node
        self.doubly_linked_list = DoublyLinkedList()

    def get(self, key):
        if key not in self.cache:
            return None
        node = self.cache[key]
        self.doubly_linked_list.detach_node(node)
        self.doubly_linked_list.add_node_to_head(node)
        return self.doubly_linked_list.algorithm.get_data(node)

    def put(self, key, value):
        if key not in self.cache:
            if self.doubly_linked_list.size == self.capacity:
                del self.cache[self.doubly_linked_list.tail.key]
                self.doubly_linked_list.detach_node(self.doubly_linked_list.tail)
            node = self.doubly_linked_list.algorithm.new_node(data=value)
            node.__dict__["key"] = key
            self.doubly_linked_list.add_node_to_head(node)
            self.cache[key] = node
        else:
            node = self.cache[key]
            self.doubly_linked_list.algorithm.set_data(node=node, data=value)
            self.doubly_linked_list.detach_node(node)
            self.doubly_linked_list.add_node_to_head(node)
