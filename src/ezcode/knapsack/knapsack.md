# Knapsack

## Question I
Given n items with weight W<sub>i</sub> and a knapsack with capacity C.<br>
How full can you fill this knapsack?
e.g. capacity = 10, weights = \[3, 4, 8, 5\]
```
>>> from ezcode.knapsack import Knapsack
>>> capacity = 10
>>> weights = [3, 4, 8, 5]
>>> values = weights
>>> Knapsack.best_value(capacity=capacity, weights=weights, values=values, fill_to_capacity=False)
(9, [1, 3])

# Explanation:
# We can fill this knapsack to weight 9 with item[1] and item[3] 
```