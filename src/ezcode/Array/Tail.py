from collections import deque


def tail_lines(file_object, lines: int = 0, block_size: int = 256, exponential_factor: int = 2):
    """
    file_object must be open with 'b', return binary string, need to be .decode('utf-8')
    seek(offset, whence=0):
        offset:
            > 0: to the end
            < 0: to the beginning
        whence:
            0: absolute file positioning
            1: current position
            2: relative to the file's end
    tell(): current position (bytes from beginning)
    """
    if lines < 0 or block_size < 0 or exponential_factor < 0:
        raise ValueError("Negative number found")
    blocks, number_of_line_feeds = deque(), lines + 1
    file_object.seek(0, 2)  # move cursor to EOF
    position = file_object.tell()
    if position > 0:
        file_object.seek(-1, 2)
        number_of_line_feeds += 1 if file_object.read() == b'\n' else 0  # read one more line if last character is b'\n'
    while number_of_line_feeds > 0 and position > 0:
        if position > block_size:
            file_object.seek(-block_size, 1)  # -block_size: move back, 1: from current position
            blocks.appendleft(file_object.read(block_size))
        else:
            file_object.seek(0, 0)  # move cursor to the beginning
            blocks.appendleft(file_object.read(position))
        line_feeds_found, block, has_enough_line_feeds = 0, blocks[0], False
        for i in range(len(block) - 1, -1, -1):  # search backward for b'\n'
            if block[i] == 10:  # ord(b'\n') is 10
                line_feeds_found += 1
            if line_feeds_found >= number_of_line_feeds:
                blocks.popleft()
                blocks.appendleft(block[i + 1:])
                has_enough_line_feeds = True
                break
        if has_enough_line_feeds:
            break
        number_of_line_feeds -= line_feeds_found
        if position > block_size:  # back to where we were before the read
            file_object.seek(-block_size, 1)
        else:
            file_object.seek(-position, 1)
        position = file_object.tell()
        block_size = int(block_size * exponential_factor)
    return b''.join(blocks)


def tail_seek_lines(file_object, lines: int = 0, block_size: int = 256, exponential_factor: int = 2):
    if lines < 0 or block_size < 0 or exponential_factor < 0:
        raise ValueError("Negative number found")
    number_of_line_feeds = lines
    file_object.seek(0, 2)  # move cursor to EOF
    position = file_object.tell()
    if position > 0:
        file_object.seek(-1, 2)
        number_of_line_feeds += 1 if file_object.read() == b'\n' else 0  # read one more line if last character is b'\n'
    while number_of_line_feeds > 0 and position > 0:
        if position > block_size:
            file_object.seek(-block_size, 1)  # -block_size: move back, 1: from current position
            block = file_object.read(block_size)
        else:
            file_object.seek(0, 0)  # move cursor to the beginning
            block = file_object.read(position)
        line_feeds_found, has_enough_line_feeds, offset = 0, False, 0
        for i in range(len(block) - 1, -1, -1):  # search backward for b'\n'
            if block[i] == 10:  # ord(b'\n') is 10
                line_feeds_found += 1
            if line_feeds_found >= number_of_line_feeds:
                offset = len(block) - 1 - i
                has_enough_line_feeds = True
                break
        if has_enough_line_feeds:
            file_object.seek(-offset, 1)
            return
        number_of_line_feeds -= line_feeds_found
        if position > block_size:  # back to where we were before the read
            file_object.seek(-block_size, 1)
        else:
            file_object.seek(-position, 1)
        position = file_object.tell()
        block_size = int(block_size * exponential_factor)





