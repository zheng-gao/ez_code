from typing import Tuple


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
