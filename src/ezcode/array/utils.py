
def swap(array: list, i: int, j: int):
    if i != j:
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp


def is_copied(array_1, array_2):
    if type(array_1) is not list and type(array_2) is not list:
        return array_1 == array_2
    elif type(array_1) is list and type(array_2) is list:
        if len(array_1) != len(array_2):
            return False
        result = True
        for subarray_1, subarray_2 in zip(array_1, array_2):
            result = result and is_copied(subarray_1, subarray_1)
        return result
    else:
        return False


