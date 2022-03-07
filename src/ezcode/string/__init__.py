
def rotate_char(char: str, rotation_factor: int):
    """ special characters won't rotate """
    if len(char) != 1:
        raise ValueError(f"Invalid char: \"{char}\"")
    if 'a' <= char and char <= 'z':
        return chr((ord(char) - ord('a') + rotation_factor) % (ord('z') - ord('a') + 1) + ord('a'))
    if 'A' <= char and char <= 'Z':
        return chr((ord(char) - ord('A') + rotation_factor) % (ord('Z') - ord('A') + 1) + ord('A'))
    if '0' <= char and char <= '9':
        return chr((ord(char) - ord('0') + rotation_factor) % (ord('9') - ord('0') + 1) + ord('0'))
    return char

