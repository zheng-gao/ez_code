from typing import Tuple


infinities = set([float("-inf"), float("inf")])


def validate_range(
    lower_bound: int,
    upper_bound: int,
    lower_bound_range: Tuple[int, int],
    upper_bound_range: Tuple[int, int]
):
    if lower_bound < lower_bound_range[0] or lower_bound >= lower_bound_range[1]:  # right side exclusive
        raise ValueError(f"The lower bound {lower_bound} is out of range [{lower_bound_range[0]}, {lower_bound_range[1]})")
    if upper_bound < upper_bound_range[0] or upper_bound >= upper_bound_range[1]:  # right side exclusive
        raise ValueError(f"The upper bound {upper_bound} is out of range [{upper_bound_range[0]}, {upper_bound_range[1]})")
    if lower_bound > upper_bound:
        raise ValueError(f"The lower bound is greater than the upper bound: {lower_bound} > {upper_bound}")


def validate_non_negative_range(
    lower_bound: int,
    upper_bound: int,
    lower_bound_range: Tuple[int, int] = (0, float("inf")),
    upper_bound_range: Tuple[int, int] = (0, float("inf"))
):
    validate_range(lower_bound, upper_bound, lower_bound_range, upper_bound_range)


def equal(collection_1, collection_2, resolution=None) -> bool:
    collection_type = type(collection_1)
    if collection_type != type(collection_2):
        return False
    if collection_type is list or collection_type is tuple:
        if len(collection_1) != len(collection_2):
            return False
        for item_1, item_2 in zip(collection_1, collection_2):
            if not equal(item_1, item_2, resolution):
                return False
        return True
    elif collection_type is set:
        if len(collection_1) != len(collection_2):
            return False
        for item in collection_1:
            if item not in collection_2:
                return False
        return True
    elif collection_type is dict:
        if len(collection_1) != len(collection_2):
            return False
        for key, value_1 in collection_1.items():
            if key not in collection_2:
                return False
            if not equal(value_1, collection_2[key], resolution):
                return False
        return True
    elif resolution is not None and collection_type is float and collection_1 not in infinities and collection_2 not in infinities:
        return abs(collection_1 - collection_2) <= resolution
    else:
        return collection_1 == collection_2

