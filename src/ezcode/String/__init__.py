
def rotate_char(char: str, rotation_factor: int) -> str:
    """ special characters won't rotate """
    if len(char) != 1:
        raise ValueError(f"Invalid char: \"{char}\"")
    valid_char, ord_char, orders = False, ord(char), [ord("0"), ord("9"), ord("a"), ord("z"), ord("A"), ord("Z")]
    for i in range(1, len(orders), 2):
        if orders[i - 1] <= ord_char and ord_char <= orders[i]:
            start, end, valid_char = orders[i - 1], orders[i], True
            break
    return chr((ord_char - start + rotation_factor) % (end - start + 1) + start) if valid_char else char


def substrings(string: str, unique: bool = True, by_size: bool = False):
    output = dict() if by_size else list()
    if unique:
        visited = set()
        for size in range(1, len(string) + 1):
            if by_size and size not in output:
                output[size] = list()
            for start in range(len(string) - size + 1):
                substring = string[start:start + size]
                if substring not in visited:
                    if by_size:
                        output[size].append(substring)
                    else:
                        output.append(substring)
                    visited.add(substring)
    else:
        for size in range(1, len(string) + 1):
            if by_size and size not in output:
                output[size] = list()
            for start in range(len(string) - size + 1):
                if by_size:
                    output[size].append(string[start:start + size])
                else:
                    output.append(string[start:start + size])
    return output


def text_justification(words: list, line_width: int) -> list:
    for word in words:
        pass
