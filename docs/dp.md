# Knapsack

Given a knapsack with capacity <strong><em>C</em></strong> and items with sizes <strong><em>S<sub>0</sub>, S<sub>1</sub>, S<sub>2</sub>, ...</em></strong>, values <strong><em>V<sub>0</sub>, V<sub>1</sub>, V<sub>2</sub>, ...</em></strong>, quantities <strong><em>Q<sub>0</sub>, Q<sub>1</sub>, Q<sub>2</sub>, ...</strong> or unlimited quantities<br>
1. [What's the max number of items can you put into the knapsack?](#q1-whats-the-max-number-of-items-can-you-put-into-the-knapsack)
2. [What's the max total size of items can you put into the knapsack?](#q2-whats-the-max-total-size-of-items-can-you-put-into-the-knapsack)
3. [What's the max total value of items can you put into the knapsack?](#q3-whats-the-max-total-value-of-items-can-you-put-into-the-knapsack)
4. [Can you fully fill the knapsack?](#q4-can-you-fully-fill-the-knapsack)
5. [What's the min/max number of items can you fully fill the knapsack?](#q5-whats-the-minmax-number-of-items-can-you-fully-fill-the-knapsack)
6. [What's the min/max total value of items can you fully fill the knapsack?](#q6-whats-the-minmax-total-value-of-items-can-you-fully-fill-the-knapsack)
7. [Find all different ways to fully fill the knapsack](#q7-find-all-different-ways-to-fully-fill-the-knapsack)<br>

## Q1. What's the max number of items can you put into the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, Q = 11, [2, 1, 5, 7], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=1, min_max=max, fill_to_capacity=False)
(3, [0, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=Q, min_max=max, fill_to_capacity=False)
(5, [0, 0, 1, 1, 2])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=None, min_max=max, fill_to_capacity=False)
(11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
```
Explanation:<br>
Set all the values to 1<br>
If each item can only be used once, we can put 3 items into the knapsack: item 0, 1, 3<br>
For limited quantity, we can put 5 items into the knapsack: item 0, 0, 1, 1, 2 (item 0 and 1 shows up twice)<br>
For unlimited quantity, we can put 11 item 1 into the knapsack<br>

## Q2. What's the max total size of items can you put into the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, Q = 11, [2, 1, 5, 7], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=1, min_max=max, fill_to_capacity=False)
(10, [0, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=Q, min_max=max, fill_to_capacity=False)
(11, [0, 1, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=None, min_max=max, fill_to_capacity=False)
(11, [1, 1, 1, 1, 3])
```
Explanation:<br>
Set the values the same as the sizes<br>
If each item can only be used once, we can fill the knapsack to size 10 with item 0, 1, 3<br>
For limited quantity, we can fill the knapsack to size 11 with item 0, 1, 1, 3 (item 1 shows up twice)<br>
For unlimited quantity, we can fill the knapsack to size 11 with item 1, 1, 1, 1, 3 (item 1 shows up 4 times)<br>

## Q3. What's the max total value of items can you put into the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, V, Q = 11, [2, 1, 5, 7], [1, 2, 2, 5], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=1, min_max=max, fill_to_capacity=False)
(8, [0, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=Q, min_max=max, fill_to_capacity=False)
(10, [0, 1, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=None, min_max=max, fill_to_capacity=False)
(22, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
```
Explanation:<br>
If each item can only be used once, we can fill the knapsack to value 8 with item 0, 1, 3<br>
For limited quantity, we can fill the knapsack to value 10 with item 0, 1, 1, 3 (item 1 shows up twice)<br>
For unlimited quantity, we can fill the knapsack to value 22 with 11 item 1<br>

## Q4. Can you fully fill the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, Q = 11, [2, 1, 5, 7], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=1, min_max=max, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=Q, min_max=max, fill_to_capacity=True)
(11, [0, 1, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=S, quantities=None, min_max=max, fill_to_capacity=True)
(11, [1, 1, 1, 1, 3])
```
Explanation:<br>
Set the values the same as the sizes<br>
If each item can only be used once, we can not fully fill the knapsack<br>
For limited quantity, we can fully fill the knapsack with item 0, 1, 1, 3 (item 1 shows up twice)<br>
For unlimited quantity, we can fully fill the knapsack with item 1, 1, 1, 1, 3 (item 1 shows up 4 times)<br>

## Q5. What's the min/max number of items can you fully fill the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, Q = 11, [2, 1, 5, 7], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=1, min_max=min, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=1, min_max=max, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=Q, min_max=min, fill_to_capacity=True)
(3, [0, 0, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=Q, min_max=max, fill_to_capacity=True)
(5, [0, 0, 1, 1, 2])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=None, min_max=min, fill_to_capacity=True)
(3, [0, 0, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=[1] * len(S), quantities=None, min_max=max, fill_to_capacity=True)
(11, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
```
Explanation:<br>
Set all the values to 1<br>
If each item can only be used once, we cannot fully fill the knapsack<br>
For limited quantity, we can fully fill the knapsack with minimum 3 items: 0, 0, 3 (item 0 shows up twice)<br>
For limited quantity, we can fully fill the knapsack with maximum 5 items: 0, 0, 1, 1, 2 (item 0 and 1 shows up twice)<br>
For unlimited quantity, we can fully fill the knapsack with minimum 3 items: 0, 0, 3 (item 0 shows up twice)<br>
For unlimited quantity, we can fully fill the knapsack with maximum 11 item 1<br>

## Q6. What's the min/max total value of items can you fully fill the knapsack?
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, V, Q = 11, [2, 1, 5, 7], [1, 2, 2, 5], [3, 2, 2, 2]
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=1, min_max=min, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=1, min_max=max, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=Q, min_max=min, fill_to_capacity=True)
(5, [0, 0, 0, 2])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=Q, min_max=max, fill_to_capacity=True)
(10, [0, 1, 1, 3])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=None, min_max=min, fill_to_capacity=True)
(5, [0, 0, 0, 2])
>>> Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=None, min_max=max, fill_to_capacity=True)
(22, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
```
Explanation:<br>
If each item can only be used once, we cannot fully fill the knapsack<br>
For limited quantity, we can fully fill the knapsack with minimum value 5: item 0, 0, 0, 2 (item 0 shows up 3 times)<br>
For limited quantity, we can fully fill the knapsack with maximum value 10: item 0, 1, 1, 3 (item 1 shows up twice)<br>
For unlimited quantity, we can fully fill the knapsack with minimum value 5: item 0, 0, 0, 2 (item 0 shows up 3 times)<br>
For unlimited quantity, we can fully fill the knapsack with maximum value 22 with 11 item 1<br>

## Q7. Find all different ways to fully fill the knapsack
```python
>>> from ezcode.dp.knapsack import Knapsack
>>> C, S, Q = 11, [2, 1, 5, 7], [3, 2, 2, 2]
>>> Knapsack.ways_to_fill(capacity=C, sizes=S, quantities=1)
(0, None)
>>> Knapsack.ways_to_fill(capacity=C, sizes=S, quantities=Q)
(5, [[0, 0, 0, 2], [0, 0, 1, 1, 2], [1, 2, 2], [0, 0, 3], [0, 1, 1, 3]])
>>> Knapsack.ways_to_fill(capacity=C, sizes=S, quantities=None)
(14, [
   [0, 0, 0, 0, 0, 1],
   [0, 0, 0, 0, 1, 1, 1],
   [0, 0, 0, 1, 1, 1, 1, 1],
   [0, 0, 1, 1, 1, 1, 1, 1, 1],
   [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
   [0, 0, 0, 2],
   [0, 0, 1, 1, 2],
   [0, 1, 1, 1, 1, 2],
   [1, 1, 1, 1, 1, 1, 2],
   [1, 2, 2],
   [0, 0, 3],
   [0, 1, 1, 3],
   [1, 1, 1, 1, 3]
])
```
Explanation:<br>
If each item can only be used once, we cannot fully fill the knapsack<br>
For limited quantity, there are 5 ways to fully fill the knapsack<br>
For unlimited quantity, there are 14 ways to fully fill the knapsack<br>

