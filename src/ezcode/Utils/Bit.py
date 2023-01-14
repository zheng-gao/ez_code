def bool_list_to_number(bool_list: list[bool], reverse=False) -> int:
    if not bool_list:
        return None
    result, length = 0, len(bool_list)
    for index, bit in enumerate(bool_list):
        result |= (bit & 1) << (index if reverse else length - index - 1)
    return result
