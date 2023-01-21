
def equal(item_1, item_2, resolution=None) -> bool:
    item_type = type(item_1)
    if item_type != type(item_2):
        return False
    if item_type is list or item_type is tuple:
        if len(item_1) != len(item_2):
            return False
        for item_1, item_2 in zip(item_1, item_2):
            if not equal(item_1, item_2, resolution):
                return False
        return True
    elif item_type is set:
        if len(item_1) != len(item_2):
            return False
        for item in item_1:
            if item not in item_2:
                return False
        return True
    elif item_type is dict:
        if len(item_1) != len(item_2):
            return False
        for key, value_1 in item_1.items():
            if key not in item_2:
                return False
            if not equal(value_1, item_2[key], resolution):
                return False
        return True
    elif resolution is not None and item_type is float and abs(item_1) != float("inf") and abs(item_2) != float("inf"):
        return abs(item_1 - item_2) <= resolution
    else:
        return item_1 == item_2

