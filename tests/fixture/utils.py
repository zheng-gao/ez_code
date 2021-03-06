
def equal_list(list_1, list_2, resolution=None):
    if type(list_1) is not list and type(list_2) is not list:
        if resolution is None:
            return list_1 == list_2
        else:
            if list_1 == float("inf") and list_2 == float("inf"):
                return True
            return abs(list_1 - list_2) <= resolution
    elif type(list_1) is list and type(list_2) is list:
        if len(list_1) != len(list_2):
            return False
        result = True
        for sublist_1, sublist_2 in zip(list_1, list_2):
            result &= equal_list(sublist_1, sublist_2, resolution)
        return result
    else:
        return False


def equal_dict(dict_1, dict_2, resolution=None):
    for key, value_1 in dict_1.items():
        if key not in dict_2:
            return False
        else:
            value_2 = dict_2[key]
            if type(value_1) is dict and type(value_2) is dict:
                if not equal_dict(value_1, value_2, resolution):
                    return False
            else:
                if resolution is None:
                    if value_1 != value_2:
                        return False
                else:
                    if value_1 != float("inf") or value_2 != float("inf"):
                        if abs(value_1 - value_2) > resolution:
                            return False
    return True
