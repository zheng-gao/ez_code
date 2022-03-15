from ezcode.knapsack import Knapsack
from fixture.utils import equal_list


def test_knapsack_with_limited_items():
    capacity, sizes, values = 4, [3, 1, 4], [20, 15, 30]

    # Limited, Not fill to capacity
    benchmark_dp_table = [
        [0,  0,  0, 20, 20],
        [0, 15, 15, 20, 35],
        [0, 15, 15, 20, 35]
    ]
    benchmark_item_list = [
        [[],  [],  [], [0],    [0]],
        [[], [1], [1], [0], [0, 1]],
        [[], [1], [1], [0], [0, 1]]
    ]
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)

    # Limited, Fill to capacity
    benchmark_dp_table = [
        [0, float("-inf"), float("-inf"), 20, float("-inf")],
        [0,            15, float("-inf"), 20,            35],
        [0,            15, float("-inf"), 20,            35]
    ]
    benchmark_item_list = [
        [[],  [], [], [0],     []],
        [[], [1], [], [0], [0, 1]],
        [[], [1], [], [0], [0, 1]]
    ]
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)


def test_knapsack_with_unlimited_items():
    capacity, sizes, values = 4, [3, 1, 4], [20, 15, 30]
    
    # Unlimited, Not fill to capacity
    benchmark_dp_table = [
        [ 0,  0,  0, 20, 20],
        [ 0, 15, 30, 45, 60],
        [ 0, 15, 30, 45, 60],
    ]
    benchmark_item_list = [
        [[],  [],     [],       [0],          [0]],
        [[], [1], [1, 1], [1, 1, 1], [1, 1, 1, 1]],
        [[], [1], [1, 1], [1, 1, 1], [1, 1, 1, 1]]
    ]
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=False, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)

    # Unlimited, Fill to capacity
    benchmark_dp_table = [
        [0, float("-inf"), float("-inf"), 20, float("-inf")],
        [0,            15,            30, 45,            60],
        [0,            15,            30, 45,            60]
    ]
    benchmark_item_list = [
        [[],  [],     [],       [0],           []],
        [[], [1], [1, 1], [1, 1, 1], [1, 1, 1, 1]],
        [[], [1], [1, 1], [1, 1, 1], [1, 1, 1, 1]]
    ]
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=max,
        fill_to_capacity=True, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)

    # Test min function
    capacity, sizes, values = 11, [5, 7], [1, 1]
    benchmark_dp_table = [
        [0, float("inf"), float("inf"), float("inf"), float("inf"), 1, float("inf"), float("inf"), float("inf"), float("inf"),2, float("inf")],
        [0, float("inf"), float("inf"), float("inf"), float("inf"), 1, float("inf"),            1, float("inf"), float("inf"),2, float("inf")],
    ]
    benchmark_item_list = [
        [[], [], [], [], [], [0], [],  [], [], [], [0, 0], []],
        [[], [], [], [], [], [0], [], [1], [], [], [0, 0], []]
    ]
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=min,
        fill_to_capacity=True, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, sizes=sizes, values=values, min_max=min,
        fill_to_capacity=True, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=min,
        fill_to_capacity=True, iterate_sizes_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, sizes=sizes, values=values, min_max=min,
        fill_to_capacity=True, iterate_sizes_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)


def test_number_of_ways_to_fill_to_capacity():
    assert 497097 == Knapsack.number_of_ways_to_fill_to_capacity_with_unlimited_items_2d(256, [1,2,4,8,16,32], False, False)

    C = 7
    S = [2,3,6,7]
    # Unlimited
    benchmark_dp_table = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 2, 1],
        [1, 0, 1, 1, 1, 1, 3, 1],
        [1, 0, 1, 1, 1, 1, 3, 2],
    ]
    benchmark_item_list = [
        [ [[]],  None,  [[0]],   None,  [[0, 0]],      None,               [[0, 0, 0]],              None ], 
        [ [[]],  None,  [[0]],  [[1]],  [[0, 0]],  [[0, 1]],       [[0, 0, 0], [1, 1]],       [[0, 0, 1]] ], 
        [ [[]],  None,  [[0]],  [[1]],  [[0, 0]],  [[0, 1]],  [[0, 0, 0], [1, 1], [2]],       [[0, 0, 1]] ], 
        [ [[]],  None,  [[0]],  [[1]],  [[0, 0]],  [[0, 1]],  [[0, 0, 0], [1, 1], [2]],  [[0, 0, 1], [3]] ]
    ]
    dp_table, item_list = Knapsack.number_of_ways_to_fill_to_capacity_with_unlimited_items_2d(
        capacity=C, sizes=S, output_dp_table=True, output_item_list=True)
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.number_of_ways_to_fill_to_capacity_with_unlimited_items_1d(
        capacity=C, sizes=S, output_dp_table=True, output_item_list=True)
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    # Limited
    benchmark_dp_table = [
        [1, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0],
        [1, 0, 1, 1, 0, 1, 1, 1]
    ]
    benchmark_item_list = [
        [ [[]],  None,  [[0]],   None,  None,      None,   None,   None ], 
        [ [[]],  None,  [[0]],  [[1]],  None,  [[0, 1]],   None,   None ], 
        [ [[]],  None,  [[0]],  [[1]],  None,  [[0, 1]],  [[2]],   None ], 
        [ [[]],  None,  [[0]],  [[1]],  None,  [[0, 1]],  [[2]],  [[3]] ], 
    ]
    dp_table, item_list = Knapsack.number_of_ways_to_fill_to_capacity_with_limited_items_2d(
        capacity=C, sizes=S, output_dp_table=True, output_item_list=True)
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.number_of_ways_to_fill_to_capacity_with_limited_items_1d(
        capacity=C, sizes=S, output_dp_table=True, output_item_list=True)
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)


def test_best_value():
    C = 10
    S = [2, 3, 5, 7]
    V = [1, 5, 2, 4]
    Q = [1, 1, 1, 1]
    assert equal_list(
        list(Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=Q, min_max=max, fill_to_capacity=False)),
        [9, [1, 3]]
    )

    C = 62
    S = [4,20,8,3,9,1,13,15,6,12,2,8,5,11,13,14,6,15,2,5,14,13,14,4,3,13,4,9,14,3]
    V = [14,79,43,115,94,128,140,95,112,167,57,106,20,109,194,176,41,51,178,80,86,169,157,131,33,15,110,184,64,84]
    Q = [16,1,19,13,1,6,16,15,19,15,4,1,4,8,14,9,1,3,18,17,17,15,7,15,14,16,15,18,17,14]
    assert equal_list(
        list(Knapsack.best_value(capacity=C, sizes=S, values=V, quantities=Q, min_max=max, fill_to_capacity=False)),
        [4719, [3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 10, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18]]
    )







