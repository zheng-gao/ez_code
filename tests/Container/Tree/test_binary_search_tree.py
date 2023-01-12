from ezcode.Container.Tree.BinarySearchTree import BinarySearchTree


class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def test_bst_validate():
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


def test_insert_and_remove():
    bst = BinarySearchTree()
    assert bst.validate()
    assert str(bst) == """
None
"""[1:]
    bst.insert(1)
    assert bst.validate()
    assert str(bst) == """
(1)
"""[1:]
    bst.insert(0)
    assert bst.validate()
    assert str(bst) == """
 ┌─(1)
(0)   
"""[1:]
    bst.insert(6)
    assert bst.validate()
    assert str(bst) == """
 ┌─(1)─┐ 
(0)   (6)
"""[1:]
    bst.insert(5)
    assert bst.validate()
    assert str(bst) == """
 ┌────(1)────┐ 
(0)       ┌─(6)
         (5)   
"""[1:]
    bst.insert(3)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────(1)──────────┐ 
(0)                ┌────(6)
                ┌─(5)      
               (3)         
"""[1:]
    bst.insert(4)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────(1)──────────────────────┐ 
(0)                                  ┌──────────(6)
                               ┌────(5)            
                              (3)─┐                
                                 (4)               
"""[1:]
    bst.insert(7)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────(1)──────────────────────┐             
(0)                                  ┌──────────(6)──────────┐ 
                               ┌────(5)                     (7)
                              (3)─┐                            
                                 (4)                           
"""[1:]
    bst.insert(2)
    assert str(bst) == """
 ┌──────────────────────(1)──────────────────────┐             
(0)                                  ┌──────────(6)──────────┐ 
                               ┌────(5)                     (7)
                            ┌─(3)─┐                            
                           (2)   (4)                           
"""[1:]
    bst.insert(9)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────(1)──────────────────────┐                   
(0)                                  ┌──────────(6)──────────┐       
                               ┌────(5)                     (7)────┐ 
                            ┌─(3)─┐                               (9)
                           (2)   (4)                                 
"""[1:]
    bst.insert(10)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────────(1)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                ┌──(3)─┐                                     (9)─┐ 
                               (2)    (4)                                      (10)
"""[1:]
    bst.insert(8)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────────(1)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                ┌──(3)─┐                                  ┌──(9)─┐ 
                               (2)    (4)                                (8)   (10)
"""[1:]
    bst.remove(1)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                    ┌─────(5)                         (7)─────┐    
                                   (3)─┐                                  ┌──(9)─┐ 
                                      (4)                                (8)   (10)
"""[1:]
    bst.remove(5)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────────────────────(2)──────────────────────────┐                         
(0)                                        ┌────────────(6)────────────┐           
                                          (3)─────┐                   (7)─────┐    
                                                 (4)                      ┌──(9)─┐ 
                                                                         (8)   (10)
"""[1:]
    bst.remove(6)
    assert bst.validate()
    assert str(bst) == """
 ┌────────────(2)────────────┐           
(0)                   ┌─────(7)─────┐    
                     (3)─┐      ┌──(9)─┐ 
                        (4)    (8)   (10)
"""[1:]
    bst.remove(10)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────(2)──────────┐       
(0)                ┌────(7)────┐ 
                  (3)─┐     ┌─(9)
                     (4)   (8)   
"""[1:]
    bst.remove(2)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────(3)──────────┐       
(0)                ┌────(7)────┐ 
                  (4)       ┌─(9)
                           (8)   
"""[1:]
    bst.remove(3)
    assert bst.validate()
    assert str(bst) == """
 ┌──────────(4)──────────┐       
(0)                     (7)────┐ 
                            ┌─(9)
                           (8)   
"""[1:]
    bst.remove(0)
    assert bst.validate()
    assert str(bst) == """
(4)──────────┐       
            (7)────┐ 
                ┌─(9)
               (8)   
"""[1:]
    bst.remove(4)
    assert bst.validate()
    assert str(bst) == """
(7)────┐ 
    ┌─(9)
   (8)   
"""[1:]
    bst.remove(9)
    assert bst.validate()
    assert str(bst) == """
(7)─┐ 
   (8)
"""[1:]
    bst.remove(7)
    assert bst.validate()
    assert str(bst) == """
(8)
"""[1:]
    bst.remove(8)
    assert bst.validate()
    assert str(bst) == """
None
"""[1:]


def test_remove_range():
    bst = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    assert str(bst) == """
           ┌────────────(5)────────────┐           
    ┌─────(3)─────┐             ┌─────(8)─────┐    
 ┌─(1)──┐        (4)           (6)─┐         (9)─┐ 
(0)    (2)                        (7)          (10)
"""[1:]
    bst.remove_range(1, 4)
    assert bst.validate()
    assert str(bst) == """
 ┌────────────(5)────────────┐           
(0)                   ┌─────(8)─────┐    
                     (6)─┐         (9)─┐ 
                        (7)          (10)
"""[1:]
    bst.remove_range(7, 9)
    assert bst.validate()
    assert str(bst) == """
 ┌─────(5)─────┐ 
(0)        ┌─(10)
          (6)    
"""[1:]
    bst.remove_range(3, 8)
    assert bst.validate()
    assert str(bst) == """
 ┌(10)
(0)   
"""[1:]
    bst.remove_range(5, 20)
    assert bst.validate()
    assert str(bst) == """
(0)
"""[1:]
    bst.remove_range(-1, 1)
    assert bst.validate()
    assert str(bst) == """
None
"""[1:]
    bst = BinarySearchTree([5, 3, 8, 4, 6, 9, 1, 0, 2, 7, 10])
    bst.remove_range(4, 7)
    assert bst.validate()
    assert str(bst) == """
           ┌────────────(8)────────────┐        
    ┌─────(3)                         (9)─────┐ 
 ┌─(1)──┐                                   (10)
(0)    (2)                                      
"""[1:]
    bst.remove_range(2, 5)
    assert bst.validate()
    assert str(bst) == """
    ┌─────(8)─────┐    
 ┌─(1)           (9)─┐ 
(0)                (10)
"""[1:]
    bst.remove_range(3, 15)
    assert bst.validate()
    assert str(bst) == """
 ┌─(1)
(0)   
"""[1:]
    bst.remove_range(0, 3)
    assert bst.validate()
    assert str(bst) == """
None
"""[1:]

