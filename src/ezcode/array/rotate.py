from ezcode.array.utils import swap


def rotate(array, shifts, is_left_rotate):

    def _rotate(array, begin, end):
        while begin < end:
            swap(array, begin, end)
            begin += 1
            end -= 1

    if array:
        size = len(array)
        shifts = shifts % size if is_left_rotate else size - shifts % size
        if shifts > 0:
            _rotate(array, 0, shifts - 1)
            _rotate(array, shifts, size - 1)
            _rotate(array, 0, size - 1)
