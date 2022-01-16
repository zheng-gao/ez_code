
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
            result &= is_copied(subarray_1, subarray_2)
        return result
    else:
        return False


def copy(array: list) -> list:
    return [copy(subarray) for subarray in array] if type(array) is list else array
        

def array_to_string(array, indent: str = "    "):
    def _array_to_string(array: list, depth: int, result: list):
        if type(array) is list:
            no_list_found = True
            for subarray in array:
                if type(subarray) is list:
                    no_list_found = False
            if no_list_found:
                result.append(f"{indent * depth}{array},\n")
            else:
                result.append(f"{indent * depth}[\n")
                for subarray in array:
                    _array_to_string(subarray, depth + 1, result)
                result.append(f"{indent * depth}]")
                result.append(",\n" if depth > 0 else "\n")
        else:
            result.append(f"{indent * depth}{array},\n")
    result = list()
    _array_to_string(array, 0, result)
    return "".join(result)


def print_array(array, indent: str = "    "):
    print(array_to_string(array, indent))