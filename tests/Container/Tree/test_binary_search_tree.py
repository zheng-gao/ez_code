from ezcode.Container.Tree.BinarySearchTree import BinarySearchTree


class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def test_binary_search_tree_validate():
    assert BinarySearchTree(root=None).validate()
    assert BinarySearchTree(root=Node(1)).validate()
    assert BinarySearchTree(root=Node(1, Node(0))).validate()
    assert BinarySearchTree(root=Node(1, None, Node(2))).validate()
    assert BinarySearchTree(root=Node(1, Node(0), Node(2))).validate()
    assert not BinarySearchTree(root=Node(1, Node(2))).validate()
    assert not BinarySearchTree(root=Node(1, None, Node(0))).validate()
    assert not BinarySearchTree(root=Node(2, Node(1), Node(0))).validate()
    assert not BinarySearchTree(root=Node(2, Node(1), Node(2))).validate()
    assert not BinarySearchTree(root=Node(2, Node(1, Node(0), Node(3)))).validate()
    assert not BinarySearchTree(root=Node(1, None, Node(2, Node(0), Node(3)))).validate()


def test_binary_search_tree_insert():
    bst = BinarySearchTree()
    assert bst.validate()
    assert len(bst) == 0
    assert str(bst) == """
None
"""[1:]
    benchmarks = [
"""
(1)
""", """
 ┌─(1)
(0)   
""", """
 ┌─(1)─┐ 
(0)   (6)
""", """
 ┌────(1)────┐ 
(0)       ┌─(6)
         (5)   
""", """
 ┌──────────(1)──────────┐ 
(0)                ┌────(6)
                ┌─(5)      
               (3)         
""", """
 ┌──────────────────────(1)──────────────────────┐ 
(0)                                  ┌──────────(6)
                               ┌────(5)            
                              (3)─┐                
                                 (4)               
""", """
 ┌──────────────────────(1)──────────────────────┐             
(0)                                  ┌──────────(6)──────────┐ 
                               ┌────(5)                     (7)
                              (3)─┐                            
                                 (4)                           
""", """
 ┌──────────────────────(1)──────────────────────┐             
(0)                                  ┌──────────(6)──────────┐ 
                               ┌────(5)                     (7)
                            ┌─(3)─┐                            
                           (2)   (4)                           
""", """
 ┌──────────────────────(1)──────────────────────┐                   
(0)                                  ┌──────────(6)──────────┐       
                               ┌────(5)                     (7)────┐ 
                            ┌─(3)─┐                               (9)
                           (2)   (4)                                 
""", """
 ┌──────────────────────────(1)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                ┌──(3)─┐                                     (9)─┐ 
                               (2)    (4)                                      (10)
""", """
 ┌──────────────────────────(1)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                ┌──(3)─┐                                  ┌──(9)─┐ 
                               (2)    (4)                                (8)   (10)
"""
    ]
    for size, (data, benchmark) in enumerate(zip([1, 0, 6, 5, 3, 4, 7, 2, 9, 10, 8], benchmarks), start=1):
        bst.insert(data)
        assert bst.validate()
        assert len(bst) == size
        assert str(bst) == benchmark[1:]
        

def test_binary_search_tree_remove():
    benchmarks = [
"""
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                   (3)─┐                                  ┌──(9)─┐ 
                                      (4)                                (8)   (10)
""", """
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                          (3)─────┐                   (7)─────┐    
                                                 (4)                      ┌──(9)─┐ 
                                                                         (8)   (10)
""", """
 ┌────────────(2)────────────┐           
(0)                   ┌─────(7)─────┐    
                     (3)─┐      ┌──(9)─┐ 
                        (4)    (8)   (10)
""", """
 ┌──────────(2)──────────┐       
(0)                ┌────(7)────┐ 
                  (3)─┐     ┌─(9)
                     (4)   (8)   
""", """
 ┌──────────(3)──────────┐       
(0)                ┌────(7)────┐ 
                  (4)       ┌─(9)
                           (8)   
""", """
 ┌──────────(4)──────────┐       
(0)                     (7)────┐ 
                            ┌─(9)
                           (8)   
""", """
(4)──────────┐       
            (7)────┐ 
                ┌─(9)
               (8)   
""", """
(7)────┐ 
    ┌─(9)
   (8)   
""", """
(7)─┐ 
   (8)
""", """
(8)
""", """
None
"""
    ]
    bst = BinarySearchTree([1, 0, 6, 5, 3, 4, 7, 2, 9, 8, 10])
    size = 11
    assert len(bst) == size
    for i, (data, benchmark) in enumerate(zip([1, 5, 6, 10, 2, 3, 0, 4, 9, 7, 8], benchmarks), start=1):
        bst.remove(data)
        assert bst.validate()
        assert len(bst) == size - i
        assert str(bst) == benchmark[1:]


def test_binary_search_tree_remove_range():
    benchmarks = [
"""
           ┌────────────(5)────────────┐           
    ┌─────(3)─────┐             ┌─────(8)─────┐    
 ┌─(1)──┐        (4)           (6)─┐         (9)─┐ 
(0)    (2)                        (7)          (10)
""", """
           ┌────────────(5)────────────┐           
    ┌─────(3)─────┐             ┌─────(8)─────┐    
 ┌─(2)           (4)           (6)─┐         (9)─┐ 
(0)                               (7)          (10)
""", """
 ┌────────────(5)────────────┐           
(0)                   ┌─────(8)─────┐    
                     (6)─┐         (9)─┐ 
                        (7)          (10)
""", """
 ┌────────────(6)────────────┐           
(0)                   ┌─────(8)─────┐    
                     (7)           (9)─┐ 
                                     (10)
""", """
 ┌─(6)─┐ 
(0)  (10)
""", """
 ┌(10)
(0)   
""", """
(0)
""", """
None
"""
]
    bst = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    for r, size, benchmark in zip(
        [(1, 1), (1, 4), (5, 5), (7, 9), (3, 8), (5, 20), (-1, 1), (0, 0)],
        [11, 10, 7, 6, 3, 2, 1, 0, 0],
        benchmarks
    ):
        assert str(bst) == benchmark[1:]
        assert bst.validate()
        assert len(bst) == size
        bst.remove_range(*r)

    benchmarks = [
"""
           ┌────────────(5)────────────┐           
    ┌─────(3)─────┐             ┌─────(8)─────┐    
 ┌─(1)──┐        (4)           (6)─┐         (9)─┐ 
(0)    (2)                        (7)          (10)
""", """
           ┌────────────(8)────────────┐        
    ┌─────(3)                         (9)─────┐ 
 ┌─(1)──┐                                   (10)
(0)    (2)                                      
""", """
    ┌─────(8)─────┐    
 ┌─(1)           (9)─┐ 
(0)                (10)
""", """
 ┌─(1)
(0)   
""", """
None
"""
]
    bst = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    for r, size, benchmark in zip(
        [(4, 7), (2, 5), (3, 15), (0, 3), (0, 0)],
        [11, 7, 5, 2, 0, 0],
        benchmarks
    ):
        assert str(bst) == benchmark[1:]
        assert bst.validate()
        assert len(bst) == size
        bst.remove_range(*r)


def test_binary_search_tree_copy():
    bst_1 = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    bst_2 = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    assert bst_1 == bst_2
    bst_3 = bst_2.copy()
    assert bst_1 == bst_3
    assert type(bst_3) is BinarySearchTree


def test_binary_search_tree_pop():
    bst_1 = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    bst_2 = bst_1.copy()
    size = len(bst_1)
    for i in range(size):
        assert bst_1.pop() == i
        assert bst_2.pop(reverse=True) == size - i - 1
 

