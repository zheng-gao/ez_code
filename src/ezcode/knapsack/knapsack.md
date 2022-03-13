# Knapsack

## Question I
Given n items with weight W<sub>i</sub><br>
How full can you fill a knapsack with capacity C.?<br>
(e.g. capacity = 10, weights = \[3, 4, 8, 5\])
```
>>> from ezcode.knapsack import Knapsack
>>> capacity = 10
>>> weights = [3, 4, 8, 5]
>>> values = weights
>>> Knapsack.best_value(
...     capacity=capacity,
...     weights=weights,
...     values=values,
...     min_max_function=max,
...     item_reusable=False,
...     fill_to_capacity=False
... )
(9, [1, 3])
```
Explanation:
We can fill this knapsack to weight 9 with item\[1\] (weight: 4) and item\[3\] (weight: 5)

## Question II
Given n items with weight W<sub>i</sub> and value V<sub>i</sub>.<br>
What's the maximum value can you put into a knapsack with capacity C?<br>
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```
>>> from ezcode.knapsack import Knapsack
>>> capacity = 10
>>> weights = [2, 3, 5, 7]
>>> values = [1, 5, 2, 4]
>>> Knapsack.best_value(
...     capacity=capacity,
...     weights=weights,
...     values=values,
...     item_reusable=False,
...     fill_to_capacity=False
... )
(9, [1, 3])
```
Explanation:
The maximum we can get is 9 with item\[1\] (weight: 3, value: 5) and item\[3\] (weight: 7, value: 4)


