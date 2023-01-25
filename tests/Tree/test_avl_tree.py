from ezcode.Random.Shuffle import knuth_shuffle
from ezcode.Tree.AVLTree import AVLTree


class Node:
    def __init__(self, height=1, data=None, left=None, right=None):
        self.height = height
        self.data = data
        self.left = left
        self.right = right


def test_avl_tree_validate():
    assert AVLTree().validate()
    assert AVLTree(root=Node()).validate()
    assert not AVLTree(root=Node(height=0)).validate()
    n = [
        Node(data=0, height=1), Node(data=1, height=2),
        Node(data=2, height=1), Node(data=3, height=3), 
        Node(data=4, height=2), Node(data=5, height=4),
        Node(data=6, height=2), Node(data=7, height=1)
    ]
    n[1].left = n[0]
    n[1].right = n[2]
    n[3].left = n[1]
    n[3].right = n[4]
    n[5].left = n[3]
    n[5].right = n[6]
    n[6].right = n[7]
    t = AVLTree(root=n[5])
    assert str(t) == """
                           ┌────────────────────────(5|H:4|B:1)────────────────────────┐                    
            ┌─────────(3|H:3|B:0)─────────┐                                      (6|H:2|B:-1)─────────┐     
     ┌─(1|H:2|B:0)──┐                (4|H:2|B:0)                                                 (7|H:1|B:0)
(0|H:1|B:0)    (2|H:1|B:0)                                                                                  
"""[1:]
    assert not t.validate()  # (4|H:2|B:0) has invalid height 2
    n[4].height = 1
    assert t.validate()
    n[4].height, n[4].left, n[1].right = 2, n[2], None
    assert str(t) == """
                           ┌────────────────────────(5|H:4|B:1)────────────────────────┐                    
            ┌─────────(3|H:3|B:0)─────────┐                                      (6|H:2|B:-1)─────────┐     
     ┌─(1|H:2|B:1)                 ┌─(4|H:2|B:1)                                                 (7|H:1|B:0)
(0|H:1|B:0)                   (2|H:1|B:0)                                                                   
"""[1:]
    assert not t.validate()  # not binary searchable
    n[1].right, n[4].left, n[5].right = n[2], None, None
    assert str(t) == """
                          ┌──────────────────────(5|H:4|B:3)
            ┌────────(3|H:3|B:0)────────┐                   
     ┌─(1|H:2|B:0)─┐               (4|H:2|B:0)              
(0|H:1|B:0)   (2|H:1|B:0)                                   
"""[1:]
    assert not t.validate()  # Unbalanced


def test_avl_tree_insert():
    t = AVLTree()
    t.validate()
    insert_benchmarks = [
"""
(5|H:1|B:0)
""","""
     ┌─(5|H:2|B:1)
(2|H:1|B:0)       
""","""
     ┌─(4|H:2|B:0)─┐     
(2|H:1|B:0)   (5|H:1|B:0)
""","""
      ┌─────────(4|H:3|B:1)─────────┐     
(2|H:2|B:-1)──┐                (5|H:1|B:0)
         (3|H:1|B:0)                      
""","""
            ┌────────(4|H:3|B:1)────────┐     
     ┌─(2|H:2|B:0)─┐               (5|H:1|B:0)
(0|H:1|B:0)   (3|H:1|B:0)                     
""","""
      ┌─────────(2|H:3|B:0)─────────┐            
(0|H:2|B:-1)──┐             ┌──(4|H:2|B:0)─┐     
         (1|H:1|B:0)   (3|H:1|B:0)    (5|H:1|B:0)
""","""
      ┌───────────────────────(2|H:4|B:-1)────────────────────────┐                           
(0|H:2|B:-1)─────────┐                             ┌────────(4|H:3|B:-1)─────────┐            
                (1|H:1|B:0)                   (3|H:1|B:0)                  (5|H:2|B:-1)─┐     
                                                                                   (6|H:1|B:0)
""","""
      ┌───────────────────────(2|H:4|B:-1)────────────────────────┐                           
(0|H:2|B:-1)─────────┐                             ┌────────(4|H:3|B:-1)─────────┐            
                (1|H:1|B:0)                   (3|H:1|B:0)                ┌──(6|H:2|B:0)─┐     
                                                                    (5|H:1|B:0)    (8|H:1|B:0)
""","""
      ┌───────────────────────(2|H:4|B:-1)────────────────────────┐                    
(0|H:2|B:-1)─────────┐                             ┌─────────(6|H:3|B:0)─────────┐     
                (1|H:1|B:0)                ┌──(4|H:2|B:0)─┐              ┌──(8|H:2|B:1)
                                      (3|H:1|B:0)    (5|H:1|B:0)    (7|H:1|B:0)        
"""
    ]
    for i, v in enumerate([5, 2, 4, 3, 0, 1, 6, 8, 7]):
        print(f"Before insert {v}")
        t.print()
        t.insert(v)
        print(f"After insert {v}")
        t.print()
        t.validate()
        assert str(t) == insert_benchmarks[i][1:]


def test_avl_tree_remove():
    t = AVLTree(init_data=[5, 2, 4, 3, 0, 1, 6, 8, 7])
    assert str(t) == """
      ┌───────────────────────(2|H:4|B:-1)────────────────────────┐                    
(0|H:2|B:-1)─────────┐                             ┌─────────(6|H:3|B:0)─────────┐     
                (1|H:1|B:0)                ┌──(4|H:2|B:0)─┐              ┌──(8|H:2|B:1)
                                      (3|H:1|B:0)    (5|H:1|B:0)    (7|H:1|B:0)        
"""[1:]
    remove_benchmarks = [
"""
      ┌───────────────────────(2|H:4|B:-1)────────────────────────┐                    
(0|H:2|B:-1)─────────┐                             ┌─────────(6|H:3|B:0)─────────┐     
                (1|H:1|B:0)                ┌──(5|H:2|B:1)                ┌──(8|H:2|B:1)
                                      (3|H:1|B:0)                   (7|H:1|B:0)        
""","""
      ┌───────────────────────(3|H:4|B:-1)────────────────────────┐                    
(0|H:2|B:-1)─────────┐                             ┌────────(6|H:3|B:-1)─────────┐     
                (1|H:1|B:0)                   (5|H:1|B:0)                ┌──(8|H:2|B:1)
                                                                    (7|H:1|B:0)        
""","""
            ┌────────(6|H:3|B:0)────────┐     
     ┌─(3|H:2|B:0)─┐             ┌─(8|H:2|B:1)
(1|H:1|B:0)   (5|H:1|B:0)   (7|H:1|B:0)       
""","""
            ┌────────(7|H:3|B:1)────────┐     
     ┌─(3|H:2|B:0)─┐               (8|H:1|B:0)
(1|H:1|B:0)   (5|H:1|B:0)                     
""","""
            ┌────────(7|H:3|B:1)────────┐     
     ┌─(3|H:2|B:1)                 (8|H:1|B:0)
(1|H:1|B:0)                                   
""","""
     ┌─(3|H:2|B:0)─┐     
(1|H:1|B:0)   (7|H:1|B:0)
""","""
     ┌─(7|H:2|B:1)
(1|H:1|B:0)       
""","""
(7|H:1|B:0)
""","""
None
"""
    ]
    for i, v in enumerate([4, 2, 0, 6, 5, 8, 3, 1, 7]):
        t.remove(v)
        assert t.validate()
        assert str(t) == remove_benchmarks[i][1:]
    t.validate()


def test_avl_tree_random_insert_and_remove():
    test_size = 300
    insert_list = knuth_shuffle([x for x in range(test_size)])
    remove_list = knuth_shuffle([x for x in range(test_size)])
    print(f"insert_list = {insert_list}\nremove_list = {remove_list}")
    t = AVLTree()
    for v in insert_list:
        t.insert(v)
        assert t.validate()
    for v in remove_list:
        t.remove(v)
        assert t.validate()


def test_avl_tree_iterator():
    benchmark = [4, 2, 0, 6, 5, 8, 3, 1, 7]
    t = AVLTree(benchmark)
    assert sorted(benchmark) == list(iter(t))
    assert sorted(benchmark, reverse=True) == list(reversed(t))

