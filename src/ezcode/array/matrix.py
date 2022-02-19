

def init_matrix(row: int, col: int, init=None) -> list[list]:
    return [[init] * col for _ in range(row)]


class MatrixIterator:
    def __init__(self, matrix: List[list], row: int = 0, col: int = 0, direction: str="horizontal"):
        self.matrix = matrix
        self.row_len = len(matrix)
        self.col_len = len(matrix[0])
        self.row = row
        self.col = col
        self.direction = direction
        self.valid_directions = {"horizontal", "vertical", "ascending-diagonal", "descending-diagonal"}
        if direction not in self.valid_directions:
            raise ValueError(f"Invalid direction \"{self.direction}\", choose from {self.valid_directions}")

    def __iter__(self):
        return self

    def __next__(self):
        if self.direction == "horizontal":
            if self.col < self.col_len:
                data = self.matrix[self.row][self.col]
                self.col += 1
                return data
        elif self.direction == "vertical":
            if self.row < self.row_len:
                data = self.matrix[self.row][self.col]
                self.row += 1
                return data
        elif self.direction == "ascending-diagonal":
            if self.row >= 0 and self.col < self.col_len:
                data = self.matrix[self.row][self.col]
                self.row -= 1
                self.col += 1
                return data
        else:  # "descending-diagonal"
            if self.row < self.row_len and self.col < self.col_len:
                data = self.matrix[self.row][self.col]
                self.row += 1
                self.col += 1
                return data
        raise StopIteration