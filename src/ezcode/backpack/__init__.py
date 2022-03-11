class Backpack:

    @staticmethod
    def max_value_2d(capacity: int, weights: list(), values: list(), iterate_weights_first=True):
        """
            0-1 Backpack
            Bag Capacity = C
            Items Weight = [w0, w1, ... ]
            Items Value  = [v0, v1, ... ]

            2D-Array "max_value" Init
            Cap=[0, 1, 2, ... c_j-1, c_j, ..., C]
            w_0  0, 0, 0, ... 0,     v_0, ..., v_0 (where c_j-1 < w0 < c_j)
            w_1  0,
            ...  0,  Max Value
            w_i  0,  Other cells will be overwritten later
            ...  0,
            w_N  0,

            The meaning of max_value[i][c]:
            Given the FIRST "i + 1" items, the max value of a bag of size "c" can make

            value_without_item_i = max_value[i-1][c]
            value_with_item_i = max_value[i - 1][c - w[i]] + v[i]

            max_value[i - 1][c - w[i]] means if we put item i into the bag (+v[i]),
            the max value that the rest of the capacity "c - w[i]" can make with a selection of the previous items

            if the capacity of the bag is not large enough for the item i, max_value[i][c] = max_value[i - 1][c]
            otherwise max_value[i][c] = max( value_without_item_i + value_with_item_i )
        """
        max_value = [[0] * (capacity + 1) for _ in range(len(weights))]
        for c in range(capacity + 1):  # init first row
            max_value[0][c] = 0 if c < weights[0] else values[0]  # c < w means the bag is empty
        if iterate_weights_first:  # we can iterate either of the weights or capacity first
            for i in range(1, len(weights)):
                for c in range(capacity + 1):
                    if c < weights[i]:
                        max_value[i][c] = max_value[i - 1][c]
                    else:
                        max_value[i][c] = max(max_value[i - 1][c], max_value[i - 1][c - weights[i]] + values[i])
        else:
            for c in range(capacity + 1):
                for i in range(1, len(weights)):
                    if c < weights[i]:
                        max_value[i][c] = max_value[i - 1][c]
                    else:
                        max_value[i][c] = max(max_value[i - 1][c], max_value[i - 1][c - weights[i]] + values[i])
        return max_value[len(weights) - 1][capacity]

    @staticmethod
    def max_value_1d(capacity: int, weights: list(), values: list()):
        """
            Rolling dp array: copy row i-1 to row i
            We just need one row:
            max_value[c] means the max value that a bag with capacity c can make
            Each loop will overwrite the max_value[c]
            Cannot swap loops
        """
        max_value = [0] * (capacity + 1)
        for i in range(len(weights)):  # must loop item weights first, because we are rolling the rows not columns
            # c < weight[i], max_value[c] won't change
            # Capacity is looping backward, otherwise the item will be put in to the backpack multiple times
            for c in range(capacity, weights[i] - 1, -1):
                max_value[c] = max(max_value[c], max_value[c - weights[i]] + values[i])
        return max_value[capacity]

    @staticmethod
    def max_value_unlimited_items(
        capacity: int,
        weights: list(),
        values: list(),
        iterate_weights_first=True
    ):
        """ Similar to rolling row solution, but the two loops can swap the order """
        max_value = [0] * (capacity + 1)
        if iterate_weights_first:
            for i in range(len(weights)):
                for c in range(weights[i], capacity + 1):  # Looping forward, so items can be added multiple times
                    max_value[c] = max(max_value[c], max_value[c - weights[i]] + values[i])
        else:
            for c in range(0, capacity + 1):  # Looping forward, so items can be added multiple times
                for i in range(len(weights)):
                    if c >= weights[i]:
                        max_value[c] = max(max_value[c], max_value[c - weights[i]] + values[i])
        return max_value[capacity]

    @staticmethod
    def best_value_with_unlimited_items(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        no_capacity_init_value=0,
        iterate_weights_first=True
    ):
        """ Similar to rolling row solution, but the two loops can swap the order """
        backpack_init_value = float("-inf") if min_max_function == max else float("inf")
        backpack_value = [backpack_init_value for _ in range(capacity + 1)]
        backpack_value[0] = no_capacity_init_value
        if iterate_weights_first:
            for i in range(len(weights)):
                for c in range(weights[i], capacity + 1):  # Looping forward, so items can be added multiple times
                    backpack_value[c] = min_max_function(backpack_value[c], backpack_value[c - weights[i]] + values[i])
        else:
            for c in range(capacity + 1):  # Looping forward, so items can be added multiple times
                for i in range(len(weights)):
                    if c >= weights[i]:
                        backpack_value[c] = min_max_function(backpack_value[c], backpack_value[c - weights[i]] + values[i])
        best_value = backpack_value[capacity]
        return best_value if best_value != backpack_init_value else None





























