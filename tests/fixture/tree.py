from ezcode.tree.binary_tree import BinaryTree
from ezcode.tree.trie import Trie, SuffixTrie
from ezcode.tree.printer import BinaryTreePrinter


class Node:
    def __init__(self, v=None, l=None, r=None):
        self.v = v
        self.l = l
        self.r = r

    def __repr__(self):
        return f"Node({self.v})"


printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
s_root = Node(0, Node(1, Node(3, r=Node(7)), Node(4)), Node(2, Node(5, Node(8), Node(9)), Node(6)))
s_tree = BinaryTree(root=s_root, data_name="v", left_name="l", right_name="r")
s_tree_print = """
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""[1:]


c_root = Node(-2, Node(8, Node(-4, l=Node(-2)), Node(3, l=Node(-1))), Node(-3, l=Node(2, Node(10), Node(7))))
c_tree = BinaryTree(root=c_root, data_name="v", left_name="l", right_name="r")
c_tree_print = """
            ┌───────────(-2)────────────┐ 
     ┌─────(8)─────┐             ┌────(-3)
  ┌(-4)         ┌─(3)        ┌──(2)─┐     
(-2)          (-1)         (10)    (7)    
"""[1:]


trie = Trie()
for word in ["code", "coke", "coffee", "cod"]:
    trie.add(word)
trie_print = """
^:4 -> c:4 -> o:4 -> d:2:$ -> e:1:$
^:4 -> c:4 -> o:4 -> k:1 -> e:1:$
^:4 -> c:4 -> o:4 -> f:1 -> f:1 -> e:1 -> e:1:$
"""[1:]

suffix_trie = SuffixTrie("abcd")
suffix_trie_print = """
^:4 -> a:1 -> b:1 -> c:1 -> d:1:$
^:4 -> b:1 -> c:1 -> d:1:$
^:4 -> c:1 -> d:1:$
^:4 -> d:1:$
"""[1:]