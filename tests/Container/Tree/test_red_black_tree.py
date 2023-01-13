from ezcode.Container.Tree.RedBlackTree import RedBlackTree


class Node:
    def __init__(self, data=None, is_red=True, parent=None, left=None, right=None):
        self.data = data
        self.is_red = is_red
        self.parent = parent
        self.left = left
        self.right = right


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


def test_red_black_tree_insert_and_remove():
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


def test_red_black_tree_iterator():
    benchmark = [4, 2, 0, 6, 5, 8, 3, 1, 7]
    t = RedBlackTree(benchmark)
    assert sorted(benchmark) == list(iter(t))
    assert sorted(benchmark, reverse=True) == list(reversed(t))


def test_red_black_tree_copy():
    t1 = RedBlackTree([4, 2, 0, 6, 5, 8, 3, 1, 7])
    t2 = RedBlackTree([4, 2, 0, 6, 5, 8, 3, 1, 7])
    assert t1 == t2
    t3 = t2.copy()
    assert t1 == t3
    assert type(t3) is RedBlackTree


