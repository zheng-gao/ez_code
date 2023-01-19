

def enumerations(item_lists: list, recursive=False) -> list:
    """
        [
            ['a', 'b'],
            ['X', 'Y'],
            [1, 2, 3],
        ]
        =>
        [
            ['a', 'X', 1],
            ['a', 'X', 2],
            ['a', 'X', 3],
            ['a', 'Y', 1],
            ['a', 'Y', 2],
            ['a', 'Y', 3],
            ['b', 'X', 1],
            ['b', 'X', 2],
            ['b', 'X', 3],
            ['b', 'Y', 1],
            ['b', 'Y', 2],
            ['b', 'Y', 3]
        ]
    """
    def _enumerations(output: list, item_lists: list, item_list: list, index: int):
        if index == len(item_list):
            output.append(item_list.copy())
        else:
            for item in item_lists[index]:
                item_list[index] = item
                _enumerations(output, item_lists, item_list, index + 1)

    if not item_lists:
        return list()
    output = list()
    if recursive:
        _enumerations(output, item_lists, [None] * len(item_lists), 0)
    else:
        stack, item_lists_size = list(), len(item_lists)
        for item in item_lists[0][::-1]:
            stack.append([item])
        while len(stack) > 0:
            template = stack.pop()
            template_size = len(template)
            if template_size == item_lists_size:
                output.append(template)
            else:
                for item in item_lists[template_size][::-1]:
                    stack.append(template + [item])
    return output










