# Knapsack

## Question I
Given n items with weight W<sub>i</sub><br>
How full can you fill a knapsack with capacity C.?<br>
(e.g. capacity = 10, weights = \[3, 4, 8, 5\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 10, [3, 4, 8, 5]
>>> Knapsack.best_value(
...     capacity=C, weights=W, values=W, quantities=([1] * len(W)),
...     min_max_function=max, fill_to_capacity=False
... )
(9, [1, 3])
```
Explanation:
We can fill this knapsack to weight 9 with item\[1\] (weight: 4) and item\[3\] (weight: 5)

## Question II
Given n items with weight W<sub>i</sub> and value V<sub>i</sub>.<br>
What's the maximum value can you put into a knapsack with capacity C?<br>
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V = 10, [2, 3, 5, 7], [1, 5, 2, 4]
>>> Knapsack.best_value(
...     capacity=C, weights=W, values=V, quantities=([1] * len(W)),
...     min_max_function=max, fill_to_capacity=False
... )
(9, [1, 3])
```
Explanation:
The maximum we can get is 9 with item\[1\] (weight: 3, value: 5) and item\[3\] (weight: 7, value: 4)

## Question III
Given n items with weight W<sub>i</sub>, value V<sub>i</sub> and quantity Q<sub>i<sub>.<br>
What's the maximum value can you put into a knapsack with capacity C?<br>
(e.g. capacity = 8, weights = \[3, 2\], values = \[30, 20\], quantities=\[1, 6\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V, Q = 8, [3, 2], [30, 20], [1, 6]
>>> Knapsack.best_value(
...     capacity=C, weights=W, values=V, quantities=Q,
...     min_max_function=max, fill_to_capacity=False
... )
(80, [1, 1, 1, 1])
```
Explanation:
The maximum we can get is 80 with 4 item\[1\] (weight: 2, value: 20)

## Question IV
Given n items with weight W<sub>i</sub>, value V<sub>i</sub> and unlimited quantity.<br>
What's the maximum value can you put into a knapsack with capacity C?<br>
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V = 10, [2, 3, 5, 7], [1, 5, 2, 4]
>>> Knapsack.best_value(
>>>     capacity=C, weights=W, values=V, quantities=None,
>>>     min_max_function=max, fill_to_capacity=False
>>> )
(15, [1, 1, 1])
```
Explanation:
The maximum we can get is 15 with 3 item[1] (weight: 3, value: 5)

## Question V
Given n items with weight W<sub>i</sub><br>
Can you exactly fill a knapsack with capacity C.?<br>
(e.g. capacity = 13, weights = \[3, 4, 9, 5\] or \[3, 2, 9, 5\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 13, [3, 4, 9, 5]
>>> Knapsack.best_value(
...     capacity=C, weights=W, values=([1] * len(W)), quantities=([1] * len(W)),
...     min_max_function=max, fill_to_capacity=True
... )
(2, [1, 2])

>>> C, W = 13, [3, 2, 9, 5]
>>> Knapsack.best_value(
...     capacity=C, weights=W, values=([1] * len(W)), quantities=([1] * len(W)),
...     min_max_function=max, fill_to_capacity=True
... )
(None, [])
```
Explanation:
1. We can exactly fill capacity 13 with 2 items, item[1] (weight: 4) and item[2] (weight: 9)
2. We cannot exactly fill capacity 13





