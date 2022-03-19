
def swap(array: list, i: int, j: int):
    if i != j:
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp


def copy(array: list) -> list:
    return [copy(subarray) for subarray in array] if type(array) is list else array


def delete_all(array: list, items_to_delete: set):
    count = 0
    for index, data in enumerate(array):
        if data in items_to_delete:
            count += 1
        elif count > 0:
            array[index - count] = data
    for _ in range(count):
        array.pop()


def array_to_string(array, indent: str = "    ", cell_size=None, right_alignment=True):
    def _array_to_string(array: list, depth: int, result: list):
        if type(array) is list:
            subarray_found = False
            for subarray in array:
                if type(subarray) is list:
                    subarray_found = True
                    break
            if not subarray_found:
                result.append(f"{indent * depth}[")
                for index, item in enumerate(array):
                    if cell_size:
                        if right_alignment:
                            item_str = str(item).rjust(cell_size, " ")
                        else:
                            item_str = str(item).ljust(cell_size, " ")
                    else:
                        item_str = str(item)
                    result.append(item_str)
                    if index < len(array) - 1:
                        result.append(", ")
                result.append("],\n")
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


def max_item_string_length(array: list):
    if isinstance(array, list):
        max_size = 0
        for subarray in array:
            max_size = max(max_item_string_length(subarray), max_size)
        return max_size
    else:
        return len(str(array))


def print_array(array, indent: str = "    ", align=True, right_alignment=True):
    max_size = max_item_string_length(array) if align else None
    print(array_to_string(array, indent, max_size, right_alignment), end="")


def split_list(original_list: list, number_of_sublists: int):
    if number_of_sublists <= 0:
        raise ValueError(f"The number_of_sublists must be positive: {number_of_sublists}")
    sublists, sublist = list(), list()
    sublist_size = len(original_list) // number_of_sublists
    items_left = len(original_list) % number_of_sublists
    sizes = [sublist_size] * number_of_sublists
    for i in range(number_of_sublists):
        if i < items_left:
            sizes[i] += 1
    for item in original_list:
        if len(sublist) < sizes[len(sublists)]:
            sublist.append(item)
        else:
            sublists.append(sublist)
            sublist = list([item])
    if sublist:
        sublists.append(sublist)
    return sublists


def split_list_generator(original_list: list, number_of_sublists: int):
    if number_of_sublists <= 0:
        raise ValueError(f"The number_of_sublists must be positive: {number_of_sublists}")
    sublists, sublist = 0, list()
    sublist_size = len(original_list) // number_of_sublists
    items_left = len(original_list) % number_of_sublists
    sizes = [sublist_size] * number_of_sublists
    for i in range(number_of_sublists):
        if i < items_left:
            sizes[i] += 1
    for item in original_list:
        if len(sublist) < sizes[sublists]:
            sublist.append(item)
        else:
            sublists += 1
            yield sublist
            sublist = list([item])
    if sublist:
        yield sublist


def chunk_list(original_list: list, chunk_size: int):
    if chunk_size <= 0:
        raise ValueError(f"The chunk_size must be positive: {chunk_size}")
    return [original_list[i:(i + chunk_size)] for i in range(0, len(original_list), chunk_size)]


def chunk_list_generator(original_list: list, chunk_size: int):
    if chunk_size <= 0:
        raise ValueError(f"The chunk_size must be positive: {chunk_size}")
    for i in range(0, len(original_list), chunk_size):
        yield original_list[i:(i + chunk_size)]
