

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


