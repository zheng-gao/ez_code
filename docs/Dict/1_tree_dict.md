# Tree Dict
```python
>>> from ezcode.Dict.TreeDict import TreeDict
>>> td = TreeDict()
>>> td[5] = "Five"
>>> td[9] = "Nine"
>>> td[3] = "Three"
>>> td[8] = "Eight"
>>> td[6] = "Six"
>>> td[1] = "One"
>>> td[0] = "Zero"
>>> td[4] = "Four"
>>> td[7] = "Seven"
>>> td[2] = "Two"
>>> list(td.keys())
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> list(td.values())
['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
>>> list(td.items())
[(0, 'Zero'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (8, 'Eight'), (9, 'Nine')]
>>> td.tree.print()

                     ┌──────────────────────────(5,'Five'|B)─────────────────────────┐                      
     ┌──────────(1,'One'|R)──────────┐                               ┌─────────(8,'Eight'|R)─────────┐      
(0,'Zero'|B)                 ┌─(3,'Three'|B)─┐                  (6,'Six'|B)──┐                  (9,'Nine'|B)
                        (2,'Two'|R)     (4,'Four'|R)                   (7,'Seven'|R)                        

>>> 8 in td
True
>>> 10 in td
False
>>> del td[10]
>>> del td[8]
>>> 8 in td
False
>>> td[4] = '4'
>>> del td[3]
>>> td[9] = 'NINE'
>>> td[2]
'Two'
>>> td[4]
'4'
>>> td[9]
'NINE'
>>> list(td.keys())
[0, 1, 2, 4, 5, 6, 7, 9]
>>> list(td.items())
[(0, 'Zero'), (1, 'One'), (2, 'Two'), (4, '4'), (5, 'Five'), (6, 'Six'), (7, 'Seven'), (9, 'NINE')]
>>> list(td.values())
['Zero', 'One', 'Two', '4', 'Five', 'Six', 'Seven', 'NINE']
>>> td.tree.print()

                     ┌──────────────────────────(5,'Five'|B)─────────────────────────┐                      
     ┌──────────(1,'One'|R)──────────┐                               ┌─────────(7,'Seven'|B)─────────┐      
(0,'Zero'|B)                 ┌───(4,'4'|B)                      (6,'Six'|R)                     (9,'NINE'|R)
                        (2,'Two'|R)                                                                         

>>> td[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/zgao/Desktop/code/ez_code/src/ezcode/Dict/TreeDict.py", line 37, in __getitem__
    raise KeyError(f"{key} not found")
KeyError: 'Key Not Found: 3'
```