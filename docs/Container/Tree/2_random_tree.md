# Random Binary Tree

```python
>>> from ezcode.tree.binary_tree import RandomBinaryTree
>>> tree = RandomBinaryTree(size=10, lower_bound=-5, upper_bound=10)
>>> tree.print()

           ┌────────────(3)────────────┐           
    ┌────(-4)─────┐                   (5)─────┐    
 ┌─(8)         ┌─(6)                      ┌──(9)─┐ 
(6)          (-2)                        (2)    (2)

>>> tree.make_tree()
>>> tree.print()

        ┌────────────(6)────────────┐        
 ┌─────(7)─────┐             ┌─────(6)─────┐ 
(9)         ┌─(1)──┐        (9)        ┌──(3)
           (1)    (5)                (10)    
```