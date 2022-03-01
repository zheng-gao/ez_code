
def swap(array: list, i: int, j: int):
    if i != j:
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp


def copy(array: list) -> list:
    return [copy(subarray) for subarray in array] if type(array) is list else array


def delete(array: list, items_to_delete: set):
    count = 0
    for index, data in enumerate(array):
        if data in items_to_delete:
            count += 1
        elif count > 0:
            array[index - count] = data
    for _ in range(count):
        array.pop()
        

def array_to_string(array, indent: str = "    "):
    def _array_to_string(array: list, depth: int, result: list):
        if type(array) is list:
            subarray_found = False
            for subarray in array:
                if type(subarray) is list:
                    subarray_found = True
                    break
            if not subarray_found:
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
    print(array_to_string(array, indent), end="")