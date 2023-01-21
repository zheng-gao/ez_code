from copy import deepcopy
from math import ceil


def init_grid(row: int, col: int, init=None) -> list[list]:
    return [[deepcopy(init) for _ in range(col)] for _ in range(row)]


def print_grid(grid: list[list], right_alignment: bool = True):
    def _find_column_max_length(grid: list):
        col_max = list()
        for col in range(len(grid[0])):
            max_length = 0
            for row in range(len(grid)):
                max_length = max(max_length, len(str(grid[row][col])))
            col_max.append(max_length)
        return col_max

    def _get_cell(string, cell_size, right_alignment=True):
        if right_alignment:
            return string.rjust(cell_size, " ")
        else:
            return string.ljust(cell_size, " ")

    col_max = _find_column_max_length(grid)
    print()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            print(_get_cell(str(grid[row][col]), col_max[col], True), end=", ")
        print()
    print()


def print_spiral(row: int, col: int, char: str = "X"):
    grids = [[" "] * col for _ in range(row)]
    rings = min(ceil(row / 2), ceil(col / 2))
    for ring in range(rings):
        if ring % 2 == 0:
            for c in range(ring - 2, col - ring):
                if c >= 0:
                    grids[ring][c] = char
            for c in range(ring, col - ring):
                if ring < rings - 1 or c == col - ring - 1:
                    grids[row - ring - 1][c] = char
    for ring in range(rings):
        if ring % 2 == 0:
            for r in range(ring + 2, row - ring):
                if ring < rings - 1 or r == row - ring - 1:
                    grids[r][ring] = char
            for r in range(ring, row - ring):
                grids[r][col - ring - 1] = char
    for line in grids:
        for grid in line:
            print(grid, end="")
        print()
