
class Trie:
    class Node:
        def __init__(self, letter, count=1):
            self.letter = letter
            self.count = count
            self.alphabet = None

    def __init__(self, first_letter="a", alphabet_size=26):
        self.first_letter = first_letter
        self.alphabet_size = alphabet_size
        self.root = self.Node(None, 0)

    def _get_next(self, node, letter):
        if not node.alphabet:
            return None
        return node.alphabet[ord(letter) - ord(self.first_letter)]

    def _set_next(self, node, letter, new_node):
        if not node.alphabet:
            node.alphabet = [None] * self.alphabet_size
        node.alphabet[ord(letter) - ord(self.first_letter)] = new_node
        return new_node

    def size(self):
        return self.root.count

    def to_string(self):
        def _pre_order(node, str_list, result):
            if node:
                str_list.append(f"{node.letter}:{node.count}")
                if not node.alphabet:
                    result.append(" -> ".join(str_list))
                else:
                    for letter_node in node.alphabet:
                        _pre_order(letter_node, str_list, result)
                str_list.pop()
        result = list()
        _pre_order(self.root, list(), result)
        return "\n".join(result) + "\n"

    def print(self):
        print(self.to_string(), end="")

    def add(self, word: str):
        self.root.count += 1
        node = self.root
        for letter in word:
            letter_node = self._get_next(node, letter)
            if letter_node:
                node = letter_node
                node.count += 1
            else:
                node = self._set_next(node, letter, self.Node(letter))

    def contains(self, word: str):
        node = self.root
        for letter in word:
            letter_node = self._get_next(node, letter)
            if not letter_node:
                return False
            node = letter_node
        return True

    def longest_common_prefix(self):
        node, prefix = self.root, list()
        while node:
            next_node = None
            if node.alphabet:
                for letter_node in node.alphabet:
                    if letter_node and letter_node.count == self.root.count:
                        prefix.append(letter_node.letter)
                        next_node = letter_node
            node = next_node
        return "".join(prefix)
