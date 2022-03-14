# Knapsack

## Question I. How full can you fill a knapsack?

### Once
Given items with weight <strong><em>W<sub>i</sub></em></strong> and each item can only be used once.<br>
How full can you fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 10, weights = \[3, 4, 8, 5\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 10, [3, 4, 8, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=W, quantities=[1] * len(W), min_max=max, fill_to_capacity=False)
(9, [1, 3])
```
Explanation:
We can fill this knapsack to weight 9 with item\[1\] (weight: 4) and item\[3\] (weight: 5)

### Multiple
Given items with weight <strong><em>W<sub>i</sub></em></strong> and quantity <strong><em>Q<sub>i</sub></em></strong>.<br>
How full can you fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 11, weights = \[3, 5, 1\], quantity = \[1, 2, 2\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, Q = 11, [3, 5, 1], [1, 2, 2]
>>> Knapsack.best_value(capacity=C, weights=W, values=W, quantities=Q, min_max=max, fill_to_capacity=False)
(11, [1, 1, 2])
```
Explanation:
We can fill this knapsack to weight 11 with 2 item\[1\] (weight: 5) and 1 item\[2\] (weight: 1)

### Unlimited
Given items with weight <strong><em>W<sub>i</sub></em></strong> and unlimited quantity of each item.<br>
How full can you fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 11, weights = \[3, 5, 2\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 11, [3, 5, 2]
>>> Knapsack.best_value(capacity=C, weights=W, values=W, quantities=None, min_max=max, fill_to_capacity=False)
(11, [0, 2, 2, 2, 2])
```
Explanation:
We can fill this knapsack to weight 11 with 1 item\[0\] (weight: 3) and 4 item\[2\] (weight: 2)

## Question II. Can you fill to the capacity?

### Once
Given items with weight <strong><em>W<sub>i</sub></em></strong> and each item can only be used once.<br>
Can you exactly fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 13, weights = \[3, 4, 9, 5\] or \[3, 2, 9, 5\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 13, [3, 4, 9, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=[1] * len(W), min_max=max, fill_to_capacity=True)
(2, [1, 2])

>>> C, W = 13, [3, 2, 9, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=[1] * len(W), min_max=max, fill_to_capacity=True)
(None, [])
```
Explanation:
1. We can exactly fill to capacity 13 with 2 items: item[1] (weight: 4) and item[2] (weight: 9)
2. We cannot exactly fill capacity 13

### Multiple
Given items with weight <strong><em>W<sub>i</sub></em></strong> and quantity <strong><em>Q<sub>i</sub></em></strong>.<br>
Can you exactly fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 13, weights = \[3, 2, 9, 5\] or \[7, 11, 9, 5\], quantities = \[2, 3, 3, 2\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, Q = 13, [3, 2, 9, 5], [2, 3, 3, 2] 
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=Q, min_max=max, fill_to_capacity=True)
(4, [0, 0, 1, 3])

>>> C, W, Q = 13, [7, 11, 9, 5], [2, 3, 3, 2]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=Q, min_max=max, fill_to_capacity=True)
(None, [])
```
Explanation:
1. We can exactly fill to capacity 13 with 4 items: 2 item[0] (weight: 3), 1 item[1] (weight: 2) and 1 item[3] (weight: 5)
2. We cannot exactly fill capacity 13 using the items

### Unlimited
Given items with weight <strong><em>W<sub>i</sub></em></strong> and unlimited quantity of each item.<br>
Can you exactly fill a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 13, weights = \[3, 2, 9, 5\] or \[7, 11, 9, 5\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 13, [3, 2, 9, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=None, min_max=max, fill_to_capacity=True)
(6, [0, 1, 1, 1, 1, 1])

>>> C, W = 13, [7, 11, 9, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=None, min_max=max, fill_to_capacity=True)
(None, [])
```
Explanation:
1. We can exactly fill to capacity 13 with 6 items: 1 item[0] (weight: 3) and 5 item[1] (weight: 2)
2. We cannot exactly fill capacity 13 using the items

## Question III. What's the maximum value can you make?

### Once
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and each item can only be used once.<br>
What's the maximum value can you put into a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V = 10, [2, 3, 5, 7], [1, 5, 2, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=[1] * len(W), min_max=max, fill_to_capacity=False)
(9, [1, 3])
```
Explanation:
The maximum we can get is 9 with item\[1\] (weight: 3, value: 5) and item\[3\] (weight: 7, value: 4)

### Multiple
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and quantity <strong><em>Q<sub>i</sub></em></strong>.<br>
What's the maximum value can you put into a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 8, weights = \[3, 2\], values = \[30, 20\], quantities=\[1, 6\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V, Q = 8, [3, 2], [30, 20], [1, 6]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=Q, min_max=max, fill_to_capacity=False)
(80, [1, 1, 1, 1])
```
Explanation:
The maximum we can get is 80 with 4 item\[1\] (weight: 2, value: 20)

### Unlimited
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and unlimited quantity of each item.<br>
What's the maximum value can you put into a knapsack with capacity <strong><em>C</em></strong>?<br>
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, V = 10, [2, 3, 5, 7], [1, 5, 2, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=None, min_max=max, fill_to_capacity=False)
(15, [1, 1, 1])
```
Explanation:
The maximum we can get is 15 with 3 item[1] (weight: 3, value: 5)

## Question IV. What's the minimum number of items and minimum value can you have when you fill to the capacity?

### Once
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and each item can only be used once.<br>
If you could exactly fill a knapsack with capacity <strong><em>C</em></strong>, what's the minimum number of items and minimum value can you have?
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 10, [2, 3, 5, 7]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=[1] * len(W), min_max=min, fill_to_capacity=True)
(2, [1, 3])

>>> C, W, V = 10, [2, 3, 5, 7], [1, 5, 2, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=[1] * len(W), min_max=min, fill_to_capacity=True)
(8, [0, 1, 2])

>>> C, W, V = 10, [2, 3, 9, 11], [1, 5, 2, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=[1] * len(W), min_max=min, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=[1] * len(W), min_max=min, fill_to_capacity=True)
(None, [])
```
Explanation:
1. When fill to capacity 10, the minimum number of items we can get is 2 with item\[1\] (weight: 3) and item\[3\] (weight: 7)
2. When fill to capacity 10, the minimum value we can get is 8 with item\[0\] (weight: 2, value: 1), item\[1\] (weight: 3, value: 5) and item\[2\] (weight: 5, value: 2)
3. We cannot fill to capacity 10 using the items
4. We cannot fill to capacity 10 using the items

### Multiple
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and quantity <strong><em>Q<sub>i</sub></em></strong>.<br>
If you could exactly fill a knapsack with capacity <strong><em>C</em></strong>, what's the minimum number of items and minimum value can you have?
(e.g. capacity = 13, weights = \[3, 2, 9, 5\] or \[7, 11, 9, 5\], values = \[1, 5, 2, 4\], quantities = \[2, 3, 3, 2\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W, Q = 13, [3, 2, 4, 9, 5], [2, 3, 3, 3, 2]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=Q, min_max=min, fill_to_capacity=True)
(2, [2, 3])

>>> C, W, V, Q = 13, [3, 2, 4, 9, 5], [2, 1, 3, 5, 4], [2, 3, 3, 3, 2]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=Q, min_max=min, fill_to_capacity=True)
(7, [1, 1, 3])

>>> C, W, V, Q = 13, [3, 2, 4, 9, 5], [2, 1, 3, 5, 4], [1, 1, 0, 3, 1]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=Q, min_max=min, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=Q, min_max=min, fill_to_capacity=True)
(None, [])
```
Explanation:
1. When fill to capacity 13, the minimum number of items we can get is 2 with item\[2\] (weight: 4) and item\[3\] (weight: 9)
2. When fill to capacity 13, the minimum value we can get is 7 with 2 item\[1\] (weight: 2, value: 1) and 1 item\[3\] (weight: 9, value: 5)
3. We cannot fill to capacity 13 using the items
4. We cannot fill to capacity 13 using the items

### Unlimited
Given items with weight <strong><em>W<sub>i</sub></em></strong>, value <strong><em>V<sub>i</sub></em></strong> and unlimited quantity of each item.<br>
If you could exactly fill a knapsack with capacity <strong><em>C</em></strong>, what's the minimum number of items and minimum value can you have?
(e.g. capacity = 10, weights = \[2, 3, 5, 7\], values = \[1, 5, 2, 4\])
(e.g. capacity = 13, weights = \[3, 2, 9, 5\] or \[7, 11, 9, 5\], values = \[1, 5, 2, 4\], quantities = \[2, 3, 3, 2\])
```python
>>> from ezcode.knapsack import Knapsack
>>> C, W = 13, [3, 2, 4, 5]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=None, min_max=min, fill_to_capacity=True)
(3, [0, 3, 3])

>>> C, W, V = 13, [3, 2, 4, 5], [2, 1, 3, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=None, min_max=min, fill_to_capacity=True)
(7, [0, 1, 1, 1, 1, 1])

>>> C, W, V = 13, [5, 10, 9, 6], [2, 1, 3, 4]
>>> Knapsack.best_value(capacity=C, weights=W, values=[1] * len(W), quantities=None, min_max=min, fill_to_capacity=True)
(None, [])
>>> Knapsack.best_value(capacity=C, weights=W, values=V, quantities=None, min_max=min, fill_to_capacity=True)
(None, [])
```
Explanation:
1. When fill to capacity 13, the minimum number of items we can get is 3 with 1 item\[0\] (weight: 3) and 2 item\[3\] (weight: 5)
2. When fill to capacity 13, the minimum value we can get is 7 with 1 item\[0\] (weight: 3, value: 2) and 5 item\[1\] (weight: 2, value: 1)
3. We cannot fill to capacity 13 using the items
4. We cannot fill to capacity 13 using the items









