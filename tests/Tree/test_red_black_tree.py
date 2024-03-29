from collections.abc import Collection
from ezcode.Random.Shuffle import knuth_shuffle
from ezcode.Tree.BinaryTree import BinaryTree
from ezcode.Tree.BinarySearchTree import BinarySearchTree
from ezcode.Tree.RedBlackTree import RedBlackTree


class Node:
    def __init__(self, data=None, is_red=True, parent=None, left=None, right=None):
        self.data = data
        self.is_red = is_red
        self.parent = parent
        self.left = left
        self.right = right


def test_red_black_tree_type():
    assert isinstance(RedBlackTree(), Collection)
    assert isinstance(RedBlackTree(), BinaryTree)
    assert isinstance(RedBlackTree(), BinarySearchTree)


def test_red_black_tree_validate():
    assert RedBlackTree().validate()
    assert RedBlackTree(root=Node(is_red=False)).validate()
    assert not RedBlackTree(root=Node(is_red=True)).validate()
    n = [Node(0), Node(1, False), Node(2), Node(3), Node(4, False), Node(5, False), Node(6, False)]
    n[0].parent = n[1]
    n[2].parent = n[1]
    n[1].left = n[0]
    n[1].right = n[2]
    n[1].parent = n[3]
    n[4].parent = n[3]
    n[3].left = n[1]
    n[3].right = n[4]
    n[3].parent = n[5]
    n[6].parent = n[5]
    n[5].left = n[3]
    n[5].right = n[6]
    t = RedBlackTree(root=n[5])
    assert str(t) == """
              ┌─────────────(5|B)─────────────┐  
      ┌─────(3|R)─────┐                     (6|B)
  ┌─(1|B)─┐         (4|B)                        
(0|R)   (2|R)                                    
"""[1:]
    assert t.validate()
    assert not t.is_balanced()  # Red Black Tree has not to be balanced
    n[1].is_red, n[3].is_red, n[4].is_red = True, False, True
    assert str(t) == """
              ┌─────────────(5|B)─────────────┐  
      ┌─────(3|B)─────┐                     (6|B)
  ┌─(1|R)─┐         (4|R)                        
(0|R)   (2|R)                                    
"""[1:]
    assert not t.validate()  # continous red
    n[0].is_red, n[2].is_red, n[4].is_red = False, False, False
    assert str(t) == """
              ┌─────────────(5|B)─────────────┐  
      ┌─────(3|B)─────┐                     (6|B)
  ┌─(1|R)─┐         (4|B)                        
(0|B)   (2|B)                                    
"""[1:]
    assert not t.validate()  # missing black nodes
    n.extend([Node(7, False), Node(8, False)])
    n[3].right = None
    n[4].parent = n[6]
    n[8].parent = n[6]
    n[6].left = n[4]
    n[6].right = n[8]
    assert str(t) == """
              ┌─────────────(5|B)─────────────┐          
      ┌─────(3|B)                     ┌─────(6|B)─────┐  
  ┌─(1|R)─┐                         (4|B)           (8|B)
(0|B)   (2|B)                                            
"""[1:]
    assert not t.validate()  # (4|B) violate binary search rule
    n[4].parent = n[3]
    n[3].right = n[4]
    n[6].left = n[7]
    n[7].parent = n[6]
    n[6].data, n[7].data = n[7].data, n[6].data
    assert str(t) == """
              ┌─────────────(5|B)─────────────┐          
      ┌─────(3|B)─────┐               ┌─────(7|B)─────┐  
  ┌─(1|R)─┐         (4|B)           (6|B)           (8|B)
(0|B)   (2|B)                                            
"""[1:]
    assert t.validate()


def test_red_black_tree_insert():
    t = RedBlackTree()
    insert_benchmarks = [
"""
(5|B)
""",
"""
  ┌─(5|B)
(2|R)    
""",
"""
  ┌─(4|B)─┐  
(2|R)   (5|R)
""",
"""
  ┌─────(4|B)─────┐  
(2|B)─┐         (5|B)
    (3|R)            
""",
"""
      ┌─────(4|B)─────┐  
  ┌─(2|B)─┐         (5|B)
(0|R)   (3|R)            
""",
"""
          ┌─────────────(4|B)─────────────┐  
  ┌─────(2|R)─────┐                     (5|B)
(0|B)─┐         (3|B)                        
    (1|R)                                    
""",
"""
          ┌─────────────(4|B)─────────────┐          
  ┌─────(2|R)─────┐                     (5|B)─────┐  
(0|B)─┐         (3|B)                           (6|R)
    (1|R)                                            
""",
"""
          ┌─────────────(4|B)─────────────┐          
  ┌─────(2|R)─────┐               ┌─────(6|B)─────┐  
(0|B)─┐         (3|B)           (5|R)           (8|R)
    (1|R)                                            
""",
"""
          ┌─────────────(4|B)─────────────┐          
  ┌─────(2|R)─────┐               ┌─────(6|R)─────┐  
(0|B)─┐         (3|B)           (5|B)         ┌─(8|B)
    (1|R)                                   (7|R)    
"""
    ]
    for i, v in enumerate([5, 2, 4, 3, 0, 1, 6, 8, 7]):
        t.insert(v)
        assert t.validate()
        assert str(t) == insert_benchmarks[i][1:]


def test_red_black_tree_remove():
    t = RedBlackTree(init_data=[5, 2, 4, 3, 0, 1, 6, 8, 7])
    assert str(t) == """
          ┌─────────────(4|B)─────────────┐          
  ┌─────(2|R)─────┐               ┌─────(6|R)─────┐  
(0|B)─┐         (3|B)           (5|B)         ┌─(8|B)
    (1|R)                                   (7|R)    
"""[1:]
    remove_benchmarks = [
"""
          ┌─────────────(5|B)─────────────┐          
  ┌─────(2|R)─────┐               ┌─────(7|R)─────┐  
(0|B)─┐         (3|B)           (6|B)           (8|B)
    (1|R)                                            
""",
"""
      ┌─────(5|B)─────┐      
  ┌─(1|R)─┐       ┌─(7|R)─┐  
(0|B)   (3|B)   (6|B)   (8|B)
""",
"""
  ┌─────(5|B)─────┐      
(1|B)─┐       ┌─(7|R)─┐  
    (3|R)   (6|B)   (8|B)
""",
"""
  ┌─────(5|B)─────┐      
(1|B)─┐         (7|B)─┐  
    (3|R)           (8|R)
""",
"""
  ┌─────(7|B)─────┐  
(1|B)─┐         (8|B)
    (3|R)            
""",
"""
  ┌─(3|B)─┐  
(1|B)   (7|B)
""",
"""
  ┌─(7|B)
(1|R)    
""",
"""
(7|B)
""",
"""
None
"""
    ]
    for i, v in enumerate([4, 2, 0, 6, 5, 8, 3, 1, 7]):
        t.remove(v)
        assert t.validate()
        assert str(t) == remove_benchmarks[i][1:]
    t.validate()


def test_red_black_tree_random_insert_and_remove():
    test_size = 300
    insert_list = knuth_shuffle([x for x in range(test_size)])
    remove_list = knuth_shuffle([x for x in range(test_size)])
    print(f"insert_list = {insert_list}\nremove_list = {remove_list}")
    t = RedBlackTree()
    for v in insert_list:
        t.insert(v)
        assert t.validate()
    for v in remove_list:
        t.remove(v)
        assert t.validate()
    t = RedBlackTree(insert_list)
    for data in sorted(insert_list):
        assert t.pop() == data


def test_red_black_tree_iterator():
    benchmark = [4, 2, 0, 6, 5, 8, 3, 1, 7]
    t = RedBlackTree(benchmark)
    assert sorted(benchmark) == list(t)
    assert sorted(benchmark, reverse=True) == list(reversed(t))


def test_red_black_tree_copy_and_equal():
    t1 = RedBlackTree([4, 2, 0, 6, 5, 8, 3, 1, 7])
    t2 = RedBlackTree([4, 2, 0, 6, 5, 8, 3, 1, 7])
    assert t1.equal(t2)
    t3 = t2.copy()
    assert t1.equal(t3)
    assert type(t3) is RedBlackTree


def test_red_black_tree_pop():
    t_1 = RedBlackTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    t_2 = t_1.copy()
    size = len(t_1)
    for i in range(size):
        assert t_1.pop() == i
        assert t_2.pop(reverse=True) == size - i - 1
    t_3 = RedBlackTree([5, 9, 3, 8, 6, 1, 0, 4, 7, 2])
    size = len(t_3)
    for i in range(size):
        assert t_3.pop() == i

