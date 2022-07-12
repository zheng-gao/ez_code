

def print_matrix(matrix: list, right_alignment=True):
    def _find_column_max_length(matrix: list):
        col_max = list()
        for col in range(len(matrix[0])):
            max_length = 0
            for row in range(len(matrix)):
                max_length = max(max_length, len(str(matrix[row][col])))
            col_max.append(max_length)
        return col_max

    def _get_cell(string, cell_size, right_alignment=True):
        if right_alignment:
            return string.rjust(cell_size, " ")
        else:
            return string.ljust(cell_size, " ")

    col_max = _find_column_max_length(matrix)
    print()
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            print(_get_cell(str(matrix[row][col]), col_max[col], True), end=", ")
        print()
    print()


def print_spiral(row, col, char="X"):
    grids = [[" "] * col for _ in range(row)]
    rings = min(math.ceil(row / 2), math.ceil(col / 2))
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
                grids[r][ring] = char
            for r in range(ring, row - ring):
                grids[r][col - ring - 1] = char
    for line in grids:
        for grid in line:
            print(grid, end="")
        print()
