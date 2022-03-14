from ezcode.knapsack import Knapsack
from fixture.utils import equal_list


def test_knapsack_with_limited_items():
    capacity, weights, values = 4, [3, 1, 4], [20, 15, 30]

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
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
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
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_limited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)


def test_knapsack_with_unlimited_items():
    capacity, weights, values = 4, [3, 1, 4], [20, 15, 30]
    
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
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=False, iterate_weights_first=False, output_dp_table=True, output_item_list=True
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
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=max,
        fill_to_capacity=True, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)

    # Test min function
    capacity, weights, values = 11, [5, 7], [1, 1]
    benchmark_dp_table = [
        [0, float("inf"), float("inf"), float("inf"), float("inf"), 1, float("inf"), float("inf"), float("inf"), float("inf"),2, float("inf")],
        [0, float("inf"), float("inf"), float("inf"), float("inf"), 1, float("inf"),            1, float("inf"), float("inf"),2, float("inf")],
    ]
    benchmark_item_list = [
        [[], [], [], [], [], [0], [],  [], [], [], [0, 0], []],
        [[], [], [], [], [], [0], [], [1], [], [], [0, 0], []]
    ]
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=min,
        fill_to_capacity=True, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_2d(
        capacity=capacity, weights=weights, values=values, min_max_function=min,
        fill_to_capacity=True, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table, dp_table) and equal_list(benchmark_item_list, item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=min,
        fill_to_capacity=True, iterate_weights_first=True, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)
    dp_table, item_list = Knapsack.best_value_with_unlimited_items_1d(
        capacity=capacity, weights=weights, values=values, min_max_function=min,
        fill_to_capacity=True, iterate_weights_first=False, output_dp_table=True, output_item_list=True
    )
    assert equal_list(benchmark_dp_table[-1], dp_table) and equal_list(benchmark_item_list[-1], item_list)












