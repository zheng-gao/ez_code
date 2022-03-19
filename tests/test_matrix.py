from ezcode.matrix import init_matrix, MatrixIterator


def test_init_matrix():
    class Data:
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return str(self.data)

    matrix = init_matrix(2, 3, Data(1))
    matrix[0][0].data = 2
    assert matrix[0][0].data == 2
    assert matrix[0][1].data == 1
    assert matrix[1][0].data == 1


def test_matrix_iterator():
    size = 4
    matrix = init_matrix(size, size)
    for row in range(size):
        for col in range(size):
            matrix[row][col] = size * row + col
    #  0  1  2  3
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15
    for row in range(size):
        iterator = MatrixIterator(matrix, row, 0, direction="horizontal")
        for col in range(size):
            assert matrix[row][col] == next(iterator)
    for col in range(size):
        iterator = MatrixIterator(matrix, 0, col, direction="vertical")
        for row in range(size):
            assert matrix[row][col] == next(iterator)
    for i in range(size):
        row_start = size - i - 1
        iterator = MatrixIterator(matrix, row_start, 0, direction="ascending-diagonal")
        for row, col in zip(range(row_start, -1, -1), range(0, i + 1)):
            assert matrix[row][col] == next(iterator)
    for i in range(size):
        iterator = MatrixIterator(matrix, 0, i, direction="descending-diagonal")
        for row, col in zip(range(0, size - i), range(i, size - i)):
            print(f"{row}, {col}")
            assert matrix[row][col] == next(iterator)





