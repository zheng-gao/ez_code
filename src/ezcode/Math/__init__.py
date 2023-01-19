def approximately_equals(value, target, error) -> bool:
    if error < 0:
        raise ValueError(f"Negative error found: {error}")
    if target < 0:
        error = -error
    return target * (1 - error) <= value and value <= target * (1 + error)
