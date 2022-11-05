from typing import Callable


class Knapsack:
    @staticmethod
    def best_value(
        capacity: int,
        sizes: list,
        values: list,
        quantities,
        min_max: Callable = max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        output_item_list=True
    ):
        """
            quantities = None (Unlimited)
            output_item_list=True -> (best_value, item_list)
            output_item_list=False -> best_value
        """
        if capacity < 0:
            raise ValueError(f"Capacity cannot be negative: {capacity}")
        for s in sizes:
            if s <= 0:
                raise ValueError(f"Item sizes must be positive: {sizes}")
        if len(sizes) != len(values):
            raise ValueError(f"The length of sizes {sizes} not match the length of values {values}")
        if quantities:
            if isinstance(quantities, list):
                if len(quantities) != len(sizes):
                    raise ValueError(f"The length of quantities {quantities} not match the length of sizes {sizes}")
                for q in quantities:
                    if q < 0:
                        raise ValueError(f"Item quantities cannot contain negative: {quantities}")
            elif quantities < 0:
                raise ValueError(f"Item quantities cannot be negative: {quantities}")
            return Knapsack.best_value_with_limited_items_1d(
                capacity=capacity,
                sizes=sizes,
                values=values,
                quantities=quantities,
                min_max=min_max,
                zero_capacity_value=zero_capacity_value,
                fill_to_capacity=fill_to_capacity,
                output_dp_table=False,
                output_item_list=output_item_list
            )
        else:
            return Knapsack.best_value_with_unlimited_items_1d(
                capacity=capacity,
                sizes=sizes,
                values=values,
                min_max=min_max,
                zero_capacity_value=zero_capacity_value,
                fill_to_capacity=fill_to_capacity,
                output_dp_table=False,
                output_item_list=output_item_list
            )

    @staticmethod
    def ways_to_fill(
        capacity: int,
        sizes: list,
        quantities,
        output_item_list=True
    ):
        """
            output_item_list=True -> (ways_to_fill, item_list)
            output_item_list=False -> ways_to_fill
        """
        if capacity < 0:
            raise ValueError(f"Capacity cannot be negative: {capacity}")
        for s in sizes:
            if s <= 0:
                raise ValueError(f"Item sizes must be positive: {sizes}")
        if quantities:
            if isinstance(quantities, list):
                if len(quantities) != len(sizes):
                    raise ValueError(f"The length of quantities {quantities} not match the length of sizes {sizes}")
                for q in quantities:
                    if q < 0:
                        raise ValueError(f"Item quantities cannot contain negative: {quantities}")
            elif quantities < 0:
                raise ValueError(f"Item quantities cannot be negative: {quantities}")
            return Knapsack.number_of_ways_to_fill_to_capacity_with_limited_items_1d(
                capacity=capacity,
                sizes=sizes,
                quantities=quantities,
                output_dp_table=False,
                output_item_list=output_item_list
            )
        else:
            return Knapsack.number_of_ways_to_fill_to_capacity_with_unlimited_items_1d(
                capacity=capacity,
                sizes=sizes,
                output_dp_table=False,
                output_item_list=output_item_list
            )

    @staticmethod
    def best_value_with_limited_items_2d(
        capacity: int,
        sizes: list,
        values: list,
        min_max: Callable = max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_sizes_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            0-1 Knapsack
            Bag Capacity = C
            Items Sizes  = [s0, s1, ... ]
            Items Values = [v0, v1, ... ]

            2D-Array "max_value" Init
            Cap=[0, 1, 2, ... c_j-1, c_j, ..., C]
            s_0  0, 0, 0, ... 0,     v_0, ..., v_0 (where c_j-1 < w0 < c_j)
            s_1  0,
            ...  0,  Max Value
            s_i  0,  Other cells will be overwritten later
            ...  0,
            s_N  0,

            The meaning of max_value[i][c]:
            Given the FIRST "i + 1" items, the max value of a bag of size "c" can make

            value_without_item_i = max_value[i-1][c]
            value_with_item_i = max_value[i - 1][c - w[i]] + v[i]

            max_value[i - 1][c - w[i]] means if we put item i into the bag (+v[i]),
            the max value that the rest of the capacity "c - w[i]" can make with a selection of the previous items

            if the capacity of the bag is not large enough for the item i, max_value[i][c] = max_value[i - 1][c]
            otherwise max_value[i][c] = max( value_without_item_i + value_with_item_i )

            if item quantity is greater than 1, expand the sizes to [q * s for q, s in zip(quantities, sizes)]

            if fill_to_capacity = True, set init value to +oo for min value or -oo for max value
            so if max_value[i - 1][c - w[i]] == oo, then max_value[i - 1][c - w[i]] + v[i] == oo
            which mean any case on the path cannot fill will make the followers not able to fill
        """
        infinity = float("-inf") if min_max == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [[knapsack_init_value for _ in range(capacity + 1)] for _ in range(len(sizes))]
        item_lists = None
        if output_item_list:
            item_lists = [[list() for _ in range(capacity + 1)] for _ in range(len(sizes))]
        for i in range(len(sizes)):  # init first column
            knapsack_value[i][0] = zero_capacity_value
        if fill_to_capacity:
            knapsack_value[0][sizes[0]] = values[0]  # init first row, c != w means not filled
            if output_item_list:
                item_lists[0][sizes[0]].append(0)
        else:
            for c in range(sizes[0], capacity + 1):  # init first row, c < w means the bag is empty
                knapsack_value[0][c] = values[0]
                if output_item_list:
                    item_lists[0][c].append(0)
        if iterate_sizes_first:  # we can iterate either of the sizes or capacity first
            for i in range(1, len(sizes)):
                for c in range(1, capacity + 1):
                    if c < sizes[i]:
                        knapsack_value[i][c] = knapsack_value[i - 1][c]
                    else:
                        knapsack_value[i][c] = min_max(knapsack_value[i - 1][c], knapsack_value[i - 1][c - sizes[i]] + values[i])
                    if output_item_list:
                        if knapsack_value[i][c] == knapsack_init_value:
                            item_lists[i][c] = list()
                        elif knapsack_value[i][c] == knapsack_value[i - 1][c]:
                            item_lists[i][c] = item_lists[i - 1][c].copy()
                        else:
                            item_lists[i][c] = item_lists[i - 1][c - sizes[i]] + [i]
        else:
            for c in range(1, capacity + 1):
                for i in range(1, len(sizes)):
                    if c < sizes[i]:
                        knapsack_value[i][c] = knapsack_value[i - 1][c]
                    else:
                        knapsack_value[i][c] = min_max(knapsack_value[i - 1][c], knapsack_value[i - 1][c - sizes[i]] + values[i])
                    if output_item_list:
                        if knapsack_value[i][c] == knapsack_init_value:
                            item_lists[i][c] = list()
                        elif knapsack_value[i][c] == knapsack_value[i - 1][c]:
                            item_lists[i][c] = item_lists[i - 1][c].copy()
                        else:
                            item_lists[i][c] = item_lists[i - 1][c - sizes[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[len(sizes) - 1][capacity]
            if output_item_list:
                item_list = item_lists[len(sizes) - 1][capacity]
                return (None, item_list) if best_value == knapsack_init_value else (best_value, item_list)
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_limited_items_1d(
        capacity: int,
        sizes: list,
        values: list,
        quantities=1,
        min_max: Callable = max,
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
        if isinstance(quantities, int):
            quantities_list = list()
            for i in range(len(sizes)):
                quantities_list.append(quantities)
            quantities = quantities_list
        else:
            assert len(sizes) == len(quantities)
        infinity = float("-inf") if min_max == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [knapsack_init_value for _ in range(capacity + 1)]
        knapsack_value[0] = zero_capacity_value
        item_lists = None
        if output_item_list:
            item_lists = [list() for _ in range(capacity + 1)]
        for i in range(len(sizes)):  # must loop item sizes first, because we are rolling the rows not columns, column step is not 1
            for q in range(1, quantities[i] + 1):  # it is same as flatten the items: sizes=[2,3] quantities=[1,2] ==> sizes=[2, 3, 3]
                # c < sizes[i], knapsack_value[c] won't change
                # Capacity is looping backward, otherwise the item will be put in to the knapsack multiple times
                for c in range(capacity, sizes[i] - 1, -1):
                    knapsack_value_without_i = knapsack_value[c - sizes[i]] + values[i]
                    knapsack_value[c] = min_max(knapsack_value[c], knapsack_value_without_i)
                    if output_item_list:
                        if knapsack_value[c] == knapsack_init_value:
                            item_lists[c] = list()
                        elif knapsack_value[c] == knapsack_value_without_i:
                            item_lists[c] = item_lists[c - sizes[i]] + [i]
                # Another solution
                # for c in range(capacity, sizes[i] - 1, -1):
                #     for q in range(1, min(quantities[i], c // sizes[i]) + 1):
                #         knapsack_value_without_i = knapsack_value[c - q * sizes[i]] + q * values[i]
                #         knapsack_value[c] = min_max(knapsack_value[c], knapsack_value_without_i)
                #         if output_item_list:
                #             if knapsack_value[c] == knapsack_init_value:
                #                 item_lists[c] = list()
                #             elif knapsack_value[c] == knapsack_value_without_i:
                #                 item_lists[c] = item_lists[c - q * sizes[i]] + [i] * q
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[capacity]
            if output_item_list:
                return (None, item_lists[capacity]) if best_value == knapsack_init_value else (best_value, item_lists[capacity])
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_unlimited_items_1d(
        capacity: int,
        sizes: list,
        values: list,
        min_max: Callable = max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_sizes_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        """ Similar to rolling row solution, but the two loops can swap the order """
        infinity = float("-inf") if min_max == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [knapsack_init_value for _ in range(capacity + 1)]
        knapsack_value[0] = zero_capacity_value
        item_lists = None
        if output_item_list:
            item_lists = [list() for _ in range(capacity + 1)]
        if iterate_sizes_first:
            for i in range(len(sizes)):
                for c in range(sizes[i], capacity + 1):  # Looping forward, so items can be added multiple times
                    knapsack_value_without_i = knapsack_value[c - sizes[i]] + values[i]
                    knapsack_value[c] = min_max(knapsack_value[c], knapsack_value_without_i)
                    if output_item_list:
                        if knapsack_value[c] == knapsack_init_value:
                            item_lists[c] = list()
                        elif knapsack_value[c] == knapsack_value_without_i:
                            item_lists[c] = item_lists[c - sizes[i]] + [i]
        else:
            for c in range(1, capacity + 1):  # Looping forward, so items can be added multiple times
                for i in range(len(sizes)):
                    if c >= sizes[i]:  # c < sizes[i], knapsack_value[c] won't change
                        knapsack_value_without_i = knapsack_value[c - sizes[i]] + values[i]
                        knapsack_value[c] = min_max(knapsack_value[c], knapsack_value_without_i)
                        if output_item_list:
                            if knapsack_value[c] == knapsack_init_value:
                                item_lists[c] = list()
                            elif knapsack_value[c] == knapsack_value_without_i:
                                item_lists[c] = item_lists[c - sizes[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[capacity]
            if output_item_list:
                return (None, item_lists[capacity]) if best_value == knapsack_init_value else (best_value, item_lists[capacity])
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def best_value_with_unlimited_items_2d(
        capacity: int,
        sizes: list,
        values: list,
        min_max: Callable = max,
        zero_capacity_value=0,
        fill_to_capacity=True,
        iterate_sizes_first=True,
        output_dp_table=False,
        output_item_list=True
    ):
        infinity = float("-inf") if min_max == max else float("inf")
        knapsack_init_value = infinity if fill_to_capacity else zero_capacity_value
        knapsack_value = [[knapsack_init_value for _ in range(capacity + 1)] for _ in range(len(sizes))]
        item_lists = None
        if output_item_list:
            item_lists = [[list() for _ in range(capacity + 1)] for _ in range(len(sizes))]
        for i in range(len(sizes)):  # init first column
            knapsack_value[i][0] = zero_capacity_value
        for c in range(sizes[0], capacity + 1):  # init first row, c < w means the bag is empty, c != w means not fill
            if c % sizes[0] == 0 or not fill_to_capacity:
                knapsack_value[0][c] = values[0] * (c // sizes[0])
                if output_item_list:
                    item_lists[0][c].extend([0] * (c // sizes[0]))
        if iterate_sizes_first:  # we can iterate either of the sizes or capacity first
            for i in range(1, len(sizes)):
                for c in range(1, capacity + 1):
                    # if c < sizes[i]:
                    #     knapsack_value[i][c] = knapsack_value[i - 1][c]
                    # else:
                    #     best_value = knapsack_init_value
                    #     for k in range(1, (c // sizes[i]) + 1):
                    #         best_value = min_max(best_value, knapsack_value[i - 1][c - k * sizes[i]] + k * values[i])
                    #     knapsack_value[i][c] = min_max(knapsack_value[i - 1][c], best_value)
                    knapsack_value[i][c] = knapsack_value[i - 1][c]  # mimic 1d
                    if output_item_list:
                        item_lists[i][c] = item_lists[i - 1][c].copy()
                    if c >= sizes[i]:
                        knapsack_value_without_i = knapsack_value[i][c - sizes[i]] + values[i]
                        knapsack_value[i][c] = min_max(knapsack_value[i][c], knapsack_value_without_i)
                        if output_item_list:
                            if knapsack_value[i][c] == knapsack_init_value:
                                item_lists[i][c] = list()
                            elif knapsack_value[i][c] == knapsack_value_without_i:
                                item_lists[i][c] = item_lists[i][c - sizes[i]] + [i]
        else:
            for c in range(1, capacity + 1):
                for i in range(1, len(sizes)):
                    # if c < sizes[i]:
                    #     knapsack_value[i][c] = knapsack_value[i - 1][c]
                    # else:
                    #     best_value = knapsack_init_value
                    #     for k in range(1, (c // sizes[i]) + 1):
                    #         best_value = min_max(best_value, knapsack_value[i - 1][c - k * sizes[i]] + k * values[i])
                    #     knapsack_value[i][c] = min_max(knapsack_value[i - 1][c], best_value)
                    knapsack_value[i][c] = knapsack_value[i - 1][c]
                    if output_item_list:
                        item_lists[i][c] = item_lists[i - 1][c].copy()
                    if c >= sizes[i]:
                        knapsack_value_without_i = knapsack_value[i][c - sizes[i]] + values[i]
                        knapsack_value[i][c] = min_max(knapsack_value[i][c], knapsack_value_without_i)
                        if output_item_list:
                            if knapsack_value[i][c] == knapsack_init_value:
                                item_lists[i][c] = list()
                            elif knapsack_value[i][c] == knapsack_value_without_i:
                                item_lists[i][c] = item_lists[i][c - sizes[i]] + [i]
        if output_dp_table:
            return (knapsack_value, item_lists) if output_item_list else knapsack_value
        else:
            best_value = knapsack_value[len(sizes) - 1][capacity]
            if output_item_list:
                item_list = item_lists[len(sizes) - 1][capacity]
                return (None, item_list) if best_value == knapsack_init_value else (best_value, item_list)
            else:
                return None if best_value == knapsack_init_value else best_value

    @staticmethod
    def number_of_ways_to_fill_to_capacity_with_unlimited_items_2d(
        capacity: int,
        sizes: list,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            number_of_ways[i][c] means given the FIRST i + 1 items, the number of ways to make capacity c
            number_of_ways[i][c] = number_of_ways[i - 1][c] + number_of_ways[i][c - sizes[i]]
        """
        number_of_ways = [[0 for _ in range(capacity + 1)] for _ in range(len(sizes))]
        combo_lists = None
        if output_item_list:
            combo_lists = [[None for _ in range(capacity + 1)] for _ in range(len(sizes))]
        for i in range(len(sizes)):  # init first column
            number_of_ways[i][0] = 1   # no item for 0 capacity is 1 way
            if output_item_list:
                combo_lists[i][0] = [[]]  # empty list for no item combo
        for c in range(sizes[0], capacity + 1):  # init first row
            if c % sizes[0] == 0:
                number_of_ways[0][c] = 1
                if output_item_list:
                    combo_lists[0][c] = [[0] * (c // sizes[0])]  # one combo of all the item 0
        for i in range(1, len(sizes)):
            for c in range(1, capacity + 1):
                number_of_ways[i][c] = number_of_ways[i - 1][c]
                if c >= sizes[i]:
                    number_of_ways[i][c] += number_of_ways[i][c - sizes[i]]  # On the same line, no i - 1
                if output_item_list:
                    combo_lists[i][c] = combo_lists[i - 1][c]
                    if c >= sizes[i] and combo_lists[i][c - sizes[i]] is not None:
                        new_combo_list = list()
                        for combo in combo_lists[i][c - sizes[i]]:
                            new_combo_list.append(combo + [i])
                        combo_lists[i][c] = combo_lists[i][c] + new_combo_list if combo_lists[i][c] is not None else new_combo_list
        if output_dp_table:
            return (number_of_ways, combo_lists) if output_item_list else number_of_ways
        else:
            best_value = number_of_ways[len(sizes) - 1][capacity]
            if output_item_list:
                combo_list = combo_lists[len(sizes) - 1][capacity]
                return (best_value, combo_list)
            else:
                return best_value

    @staticmethod
    def number_of_ways_to_fill_to_capacity_with_unlimited_items_1d(
        capacity: int,
        sizes: list,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            number_of_ways[c] means the number of ways to make capacity c
            rolling row[i-1] over to row[i]
            number_of_ways[c] = number_of_ways[c] + number_of_ways[c - sizes[i]]
        """
        number_of_ways = [0 for _ in range(capacity + 1)]
        combo_lists = None
        if output_item_list:
            combo_lists = [None for _ in range(capacity + 1)]
        number_of_ways[0] = 1  # no item for 0 capacity is 1 way
        if output_item_list:
            combo_lists[0] = [[]]  # empty list for no item combo
        for i in range(len(sizes)):
            for c in range(sizes[i], capacity + 1):  # c starts from sizes[i] (c >= sizes[i])
                number_of_ways[c] += number_of_ways[c - sizes[i]]  # + (c > sizes[i] and c % sizes[i] == 0)
                if output_item_list:
                    if combo_lists[c - sizes[i]] is not None:
                        new_combo_list = list()
                        for combo in combo_lists[c - sizes[i]]:
                            new_combo_list.append(combo + [i])
                        combo_lists[c] = combo_lists[c] + new_combo_list if combo_lists[c] is not None else new_combo_list
        if output_dp_table:
            return (number_of_ways, combo_lists) if output_item_list else number_of_ways
        else:
            best_value = number_of_ways[capacity]
            if output_item_list:
                combo_list = combo_lists[capacity]
                return (best_value, combo_list)
            else:
                return best_value

    @staticmethod
    def number_of_ways_to_fill_to_capacity_with_limited_items_2d(
        capacity: int,
        sizes: list,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            number_of_ways[i][c] means given the FIRST i items, the number of ways to make capacity c
            number_of_ways[i][c] = number_of_ways[i - 1][c] + number_of_ways[i - 1][c - sizes[i]]
            number_of_ways[i - 1][c] means without item[i], only use FIRST i - 1 items, the number of combos
            number_of_ways[i - 1][c - sizes[i]] means with item[i], every combo that make c-sizes[i] can add item[i] to get a new combo that make
        """
        number_of_ways = [[0 for _ in range(capacity + 1)] for _ in range(len(sizes))]
        combo_lists = None
        if output_item_list:
            combo_lists = [[None for _ in range(capacity + 1)] for _ in range(len(sizes))]
        for i in range(len(sizes)):  # init first column
            number_of_ways[i][0] = 1   # no item for 0 capacity is 1 way
            if output_item_list:
                combo_lists[i][0] = [[]]  # empty list for no item combo
        if sizes[0] <= capacity:  # init first row
            number_of_ways[0][sizes[0]] = 1
            if output_item_list:
                combo_lists[0][sizes[0]] = [[0]]
        for i in range(1, len(sizes)):
            for c in range(1, capacity + 1):
                # if c < sizes[i]:
                #     number_of_ways[i][c] = number_of_ways[i - 1][c]
                # elif c == sizes[i]:
                #     number_of_ways[i][c] = number_of_ways[i - 1][c] + number_of_ways[i - 1][c - sizes[i]]
                number_of_ways[i][c] = number_of_ways[i - 1][c]
                if c >= sizes[i]:
                    number_of_ways[i][c] += number_of_ways[i - 1][c - sizes[i]]
                if output_item_list:
                    if combo_lists[i - 1][c] is not None:
                        combo_lists[i][c] = combo_lists[i - 1][c]
                    if c >= sizes[i] and combo_lists[i - 1][c - sizes[i]] is not None:
                        new_combo_list = list()
                        for combo in combo_lists[i - 1][c - sizes[i]]:
                            new_combo_list.append(combo + [i])
                        combo_lists[i][c] = combo_lists[i][c] + new_combo_list if combo_lists[i][c] is not None else new_combo_list
        if output_dp_table:
            return (number_of_ways, combo_lists) if output_item_list else number_of_ways
        else:
            best_value = number_of_ways[len(sizes) - 1][capacity]
            if output_item_list:
                combo_list = combo_lists[len(sizes) - 1][capacity]
                return (best_value, combo_list)
            else:
                return best_value

    @staticmethod
    def number_of_ways_to_fill_to_capacity_with_limited_items_1d(
        capacity: int,
        sizes: list,
        quantities=1,
        output_dp_table=False,
        output_item_list=True
    ):
        """
            number_of_ways[c] means the number of ways to make capacity c
            number_of_ways[c] = number_of_ways[c] + number_of_ways[c - sizes[i]]
        """
        if isinstance(quantities, int):
            quantities_list = list()
            for i in range(len(sizes)):
                quantities_list.append(quantities)
            quantities = quantities_list
        else:
            assert len(sizes) == len(quantities)
        number_of_ways = [0 for _ in range(capacity + 1)]
        combo_lists = None
        if output_item_list:
            combo_lists = [None for _ in range(capacity + 1)]
        number_of_ways[0] = 1  # no item for 0 capacity is 1 way
        if output_item_list:
            combo_lists[0] = [[]]  # empty list for no item combo
        for i in range(len(sizes)):
            for q in range(1, quantities[i] + 1):
                for c in range(capacity, sizes[i] - 1, -1):  # c >= sizes[i]
                    number_of_ways[c] += number_of_ways[c - sizes[i]]
                    if output_item_list:
                        if combo_lists[c - sizes[i]] is not None:
                            new_combo_list = list()
                            for combo in combo_lists[c - sizes[i]]:
                                new_combo_list.append(combo + [i])
                            combo_lists[c] = combo_lists[c] + new_combo_list if combo_lists[c] is not None else new_combo_list
        if output_dp_table:
            return (number_of_ways, combo_lists) if output_item_list else number_of_ways
        else:
            best_value = number_of_ways[capacity]
            if output_item_list:
                combo_list = combo_lists[capacity]  # It might have duplicates
                unique_combo_list = list()
                if combo_list:
                    combo_set = set()
                    for i, combo in enumerate(combo_list):
                        t = tuple(sorted(combo))
                        if t not in combo_set:
                            unique_combo_list.append(combo)
                        combo_set.add(t)
                    return (len(unique_combo_list), unique_combo_list)
                return (best_value, combo_list)
            else:
                return best_value

















