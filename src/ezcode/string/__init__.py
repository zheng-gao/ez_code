
def rotate_char(char: str, rotation_factor: int):
    """ special characters won't rotate """
    if len(char) != 1:
        raise ValueError(f"Invalid char: \"{char}\"")
    start, end = "", ""
    if "0" <= char and char <= "9":
        start, end = "0", "9"
    elif "a" <= char and char <= "z":
        start, end = "a", "z"
    elif "A" <= char and char <= "Z":
        start, end = "A", "Z"
    else:
        return char
    return chr((ord(char) - ord(start) + rotation_factor) % (ord(end) - ord(start) + 1) + ord(start))

