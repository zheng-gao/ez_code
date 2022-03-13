class Knapsack:
    @staticmethod
    def best_value(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        item_reusable=False,
        output_item_list=True
    ):
        if capacity < 0:
            raise ValueError(f"Capacity cannot be negative: {capacity}")
        for w in weights:
            if w <= 0:
                raise ValueError(f"Item weight must be positive: {weights}")
        if not item_reusable:
            if min_max_function == max:
                for v in values:
                    if v < 0:
                        raise ValueError(f"Non-reusable item can only have positive value with max function: {values}")
            if min_max_function == min:
                for v in values:
                    if v > 0:
                        raise ValueError(f"Non-reusable item can only have negative value with min function: {values}")
            return Knapsack.best_value_with_non_reusable_items_1d(
                capacity=capacity,
                weights=weights,
                values=values,
                min_max_function=min_max_function,
                zero_capacity_value=zero_capacity_value,
                fill_to_capacity=fill_to_capacity,
                output_dp_table=False,
                output_item_list=output_item_list
            )
        else:
            return Knapsack.best_value_with_reusable_items_1d(
                capacity=capacity,
                weights=weights,
                values=values,
                min_max_function=min_max_function,
                zero_capacity_value=zero_capacity_value,
                fill_to_capacity=fill_to_capacity,
                output_dp_table=False,
                output_item_list=output_item_list
            )

    @staticmethod
    def best_value_with_non_reusable_items_2d(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_weights_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            0-1 Knapsack
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
        infinity = float("-inf") if min_max_function == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [[knapsack_init_value for _ in range(capacity + 1)] for _ in range(len(weights))]
        item_lists = None
        if output_item_list:
            item_lists = [[list() for _ in range(capacity + 1)] for _ in range(len(weights))]
        for i in range(len(weights)):  # init first column
            knapsack_value[i][0] = zero_capacity_value
        if fill_to_capacity:
            knapsack_value[0][weights[0]] = values[0]  # init first row, c != w means not filled
            if output_item_list:
                item_lists[0][weights[0]].append(0)
        else:
            for c in range(weights[0], capacity + 1):  # init first row, c < w means the bag is empty
                knapsack_value[0][c] = values[0]
                if output_item_list:
                    item_lists[0][c].append(0)
        if iterate_weights_first:  # we can iterate either of the weights or capacity first
            for i in range(1, len(weights)):
                for c in range(1, capacity + 1):
                    if c < weights[i]:
                        knapsack_value[i][c] = knapsack_value[i - 1][c]
                    else:
                        knapsack_value[i][c] = min_max_function(knapsack_value[i - 1][c], knapsack_value[i - 1][c - weights[i]] + values[i])
                    if output_item_list:
                        if knapsack_value[i][c] == knapsack_init_value:
                            item_lists[i][c] = list()
                        elif knapsack_value[i][c] == knapsack_value[i - 1][c]:
                            item_lists[i][c] = item_lists[i - 1][c].copy()
                        else:
                            item_lists[i][c] = item_lists[i - 1][c - weights[i]] + [i]
        else:
            for c in range(1, capacity + 1):
                for i in range(1, len(weights)):
                    if c < weights[i]:
                        knapsack_value[i][c] = knapsack_value[i - 1][c]
                    else:
                        knapsack_value[i][c] = min_max_function(knapsack_value[i - 1][c], knapsack_value[i - 1][c - weights[i]] + values[i])
                    if output_item_list:
                        if knapsack_value[i][c] == knapsack_init_value:
                            item_lists[i][c] = list()
                        elif knapsack_value[i][c] == knapsack_value[i - 1][c]:
                            item_lists[i][c] = item_lists[i - 1][c].copy()
                        else:
                            item_lists[i][c] = item_lists[i - 1][c - weights[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[len(weights) - 1][capacity]
            if output_item_list:
                item_list = item_lists[len(weights) - 1][capacity]
                return (None, item_list) if best_value == knapsack_init_value else (best_value, item_list)
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_non_reusable_items_1d(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            Rolling dp array: copy row i-1 to row i
            We just need one row:
            knapsack_value[c] means the max value that a bag with capacity c can make
            Each loop will overwrite the knapsack_value[c]
            Cannot swap loops
        """
        infinity = float("-inf") if min_max_function == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [knapsack_init_value for _ in range(capacity + 1)]
        knapsack_value[0] = zero_capacity_value
        item_lists = None
        if output_item_list:
            item_lists = [list() for _ in range(capacity + 1)]
        for i in range(len(weights)):  # must loop item weights first, because we are rolling the rows not columns
            # c < weight[i], knapsack_value[c] won't change
            # Capacity is looping backward, otherwise the item will be put in to the knapsack multiple times
            for c in range(capacity, weights[i] - 1, -1):
                knapsack_value[c] = min_max_function(knapsack_value[c], knapsack_value[c - weights[i]] + values[i])
                if output_item_list:
                    if knapsack_value[c] == knapsack_init_value:
                        item_lists[c] = list()
                    elif knapsack_value[c] == knapsack_value[c - weights[i]] + values[i]:
                        item_lists[c] = item_lists[c - weights[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[capacity]
            if output_item_list:
                return (None, item_lists[capacity]) if best_value == knapsack_init_value else (best_value, item_lists[capacity])
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_reusable_items_1d(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_weights_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        """ Similar to rolling row solution, but the two loops can swap the order """
        infinity = float("-inf") if min_max_function == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [knapsack_init_value for _ in range(capacity + 1)]
        knapsack_value[0] = zero_capacity_value
        item_lists = None
        if output_item_list:
            item_lists = [list() for _ in range(capacity + 1)]
        if iterate_weights_first:
            for i in range(len(weights)):
                for c in range(weights[i], capacity + 1):  # Looping forward, so items can be added multiple times
                    knapsack_value[c] = min_max_function(knapsack_value[c], knapsack_value[c - weights[i]] + values[i])
                    if output_item_list:
                        if knapsack_value[c] == knapsack_init_value:
                            item_lists[c] = list()
                        elif knapsack_value[c] == knapsack_value[c - weights[i]] + values[i]:
                            item_lists[c] = item_lists[c - weights[i]] + [i]
        else:
            for c in range(1, capacity + 1):  # Looping forward, so items can be added multiple times
                for i in range(len(weights)):
                    if c >= weights[i]:  # c < weight[i], knapsack_value[c] won't change
                        knapsack_value[c] = min_max_function(knapsack_value[c], knapsack_value[c - weights[i]] + values[i])
                        if output_item_list:
                            if knapsack_value[c] == knapsack_init_value:
                                item_lists[c] = list()
                            elif knapsack_value[c] == knapsack_value[c - weights[i]] + values[i]:
                                item_lists[c] = item_lists[c - weights[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[capacity]
            if output_item_list:
                return (None, item_lists[capacity]) if best_value == knapsack_init_value else (best_value, item_lists[capacity])
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_reusable_items_2d(
        capacity: int,
        weights: list(),
        values: list(),
        min_max_function=max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_weights_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        infinity = float("-inf") if min_max_function == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [[knapsack_init_value for _ in range(capacity + 1)] for _ in range(len(weights))]
        item_lists = None
        if output_item_list:
            item_lists = [[list() for _ in range(capacity + 1)] for _ in range(len(weights))]
        for i in range(len(weights)):  # init first column
            knapsack_value[i][0] = zero_capacity_value
        for c in range(weights[0], capacity + 1):  # init first row, c < w means the bag is empty, c != w means not fill
            if c % weights[0] == 0 or not fill_to_capacity:
                knapsack_value[0][c] = values[0] * (c // weights[0])
                if output_item_list:
                    item_lists[0][c].extend([0] * (c // weights[0]))
        if iterate_weights_first:  # we can iterate either of the weights or capacity first
            for i in range(1, len(weights)):
                for c in range(1, capacity + 1):
                    # if c < weights[i]:
                    #     knapsack_value[i][c] = knapsack_value[i - 1][c]
                    # else:
                    #     best_value = knapsack_init_value
                    #     for k in range(1, (c // weights[i]) + 1):
                    #         best_value = min_max_function(best_value, knapsack_value[i - 1][c - k * weights[i]] + k * values[i])
                    #     knapsack_value[i][c] = min_max_function(knapsack_value[i - 1][c], best_value)
                    knapsack_value[i][c] = knapsack_value[i - 1][c]
                    if output_item_list:
                        item_lists[i][c] = item_lists[i - 1][c].copy()
                    if c >= weights[i]:
                        knapsack_value[i][c] = min_max_function(knapsack_value[i][c], knapsack_value[i][c - weights[i]] + values[i])
                        if output_item_list:
                            if knapsack_value[i][c] == knapsack_init_value:
                                item_lists[i][c] = list()
                            elif knapsack_value[i][c] == knapsack_value[i][c - weights[i]] + values[i]:
                                item_lists[i][c] = item_lists[i][c - weights[i]] + [i]
        else:
            for c in range(1, capacity + 1):
                for i in range(1, len(weights)):
                    # if c < weights[i]:
                    #     knapsack_value[i][c] = knapsack_value[i - 1][c]
                    # else:
                    #     best_value = knapsack_init_value
                    #     for k in range(1, (c // weights[i]) + 1):
                    #         best_value = min_max_function(best_value, knapsack_value[i - 1][c - k * weights[i]] + k * values[i])
                    #     knapsack_value[i][c] = min_max_function(knapsack_value[i - 1][c], best_value)
                    knapsack_value[i][c] = knapsack_value[i - 1][c]
                    if output_item_list:
                        item_lists[i][c] = item_lists[i - 1][c].copy()
                    if c >= weights[i]:
                        knapsack_value[i][c] = min_max_function(knapsack_value[i][c], knapsack_value[i][c - weights[i]] + values[i])
                        if output_item_list:
                            if knapsack_value[i][c] == knapsack_init_value:
                                item_lists[i][c] = list()
                            elif knapsack_value[i][c] == knapsack_value[i][c - weights[i]] + values[i]:
                                item_lists[i][c] = item_lists[i][c - weights[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[len(weights) - 1][capacity]
            if output_item_list:
                item_list = item_lists[len(weights) - 1][capacity]
                return (None, item_list) if best_value == knapsack_init_value else (best_value, item_list)
            else:
                return None if best_value == knapsack_init_value else best_value



























