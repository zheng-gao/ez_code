from copy import deepcopy
from typing import List


def init_matrix(row: int, col: int, init=None) -> list[list]:
    return [[deepcopy(init) for _ in range(col)] for _ in range(row)]


class MatrixIterator:
    def __init__(self, matrix: List[list], row: int = 0, col: int = 0, direction: str="horizontal"):
        self.matrix = matrix
        self.row, self.row_min, self.row_max = row, 0, len(matrix) - 1
        self.col, self.col_min, self.col_max = col, 0, len(matrix[0]) - 1
        self.direction = direction
        self.valid_directions = {"horizontal", "vertical", "ascending-diagonal", "descending-diagonal"}
        if direction not in self.valid_directions:
            raise ValueError(f"Invalid direction \"{self.direction}\", choose from {self.valid_directions}")

    def __iter__(self):
        return self

    def __next__(self):
        data = None
        try:
            data = self.matrix[self.row][self.col]
        except IndexError:
            raise StopIteration
        if self.direction == "horizontal":
            if self.col <= self.col_max:
                self.col += 1
        elif self.direction == "vertical":
            if self.row <= self.row_max:
                self.row += 1
        elif self.direction == "ascending-diagonal":
            if self.row >= self.row_min and self.col <= self.col_max:
                self.row -= 1
                self.col += 1
        elif self.direction == "descending-diagonal":
            if self.row <= self.row_max and self.col <= self.col_max:
                self.row += 1
                self.col += 1
        return data