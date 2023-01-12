from enum import Enum


GridIteratorMode = Enum("GridIteratorMode", ["HORIZONTAL", "VERTICAL", "MAJOR_DIAGONAL", "MINOR_DIAGONAL", "SPIRAL"])


class GridIteratorFactory:
    @staticmethod
    def get(
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        mode: GridIteratorMode = GridIteratorMode.HORIZONTAL, reverse: bool = False
    ):
        if mode == GridIteratorMode.HORIZONTAL:
            return GridHorizontalIterator(grid, row_start, col_start, row_end, col_end, reverse)
        elif mode == GridIteratorMode.VERTICAL:
            return GridVerticalIterator(grid, row_start, col_start, row_end, col_end, reverse)
        elif mode == GridIteratorMode.MAJOR_DIAGONAL:
            return GridMajorDiagonalIterator(grid, row_start, col_start, row_end, col_end, reverse)
        elif mode == GridIteratorMode.MINOR_DIAGONAL:
            return GridMinorDiagonalIterator(grid, row_start, col_start, row_end, col_end, reverse)
        elif mode == GridIteratorMode.SPIRAL:
            return GridSpiralIterator(grid, row_start, col_start, row_end, col_end, reverse)
        else:
            raise NotImplementedError(f"{mode} not found")


class GridIterator:
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        self.grid, self.reverse = grid, reverse
        if not self.valid_row(row_start):
            raise IndexError(f"Invalid row_start: {row_start}")
        if not self.valid_col(col_start):
            raise IndexError(f"Invalid col_start: {col_start}")
        if row_end is not None and not self.valid_row(row_end):
            raise IndexError(f"Invalid row_end: {row_end}")
        if col_end is not None and not self.valid_col(col_end):
            raise IndexError(f"Invalid col_end: {col_end}")
        self.row, self.col, self.row_end, self.col_end = row_start, col_start, row_end, col_end

    def __iter__(self):
        return self

    def __next__(self):
        pass

    def has_next(self):
        pass

    def valid_row(self, row) -> bool:
        return 0 <= row and row < len(self.grid)

    def valid_col(self, col) -> bool:
        return 0 <= col and col < len(self.grid[0])


class GridHorizontalIterator(GridIterator):
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        """ default: Left -> Right, reverse: Right -> Left """
        if col_end is None:
            col_end = 0 if reverse else len(grid[0]) - 1
        super().__init__(grid, row_start, col_start, row_end, col_end, reverse)

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        data = self.grid[self.row][self.col]
        self.col += -1 if self.reverse else 1
        return data

    def has_next(self):
        return (self.reverse and self.col >= self.col_end) or (not self.reverse and self.col <= self.col_end)


class GridVerticalIterator(GridIterator):
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        """ default: Upper -> Lower, reverse: Lower -> Upper """
        if row_end is None:
            row_end = 0 if reverse else len(grid) - 1
        super().__init__(grid, row_start, col_start, row_end, col_end, reverse)

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        data = self.grid[self.row][self.col]
        self.row += -1 if self.reverse else 1
        return data

    def has_next(self):
        return (self.reverse and self.row >= self.row_end) or (not self.reverse and self.row <= self.row_end)


class GridMajorDiagonalIterator(GridIterator):
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        """ default: Upper Left -> Lower Right, reverse: Lower Right -> Upper Left """
        if row_end is None:
            row_end = 0 if reverse else len(grid) - 1
        if col_end is None:
            col_end = 0 if reverse else len(grid[0]) - 1
        super().__init__(grid, row_start, col_start, row_end, col_end, reverse)

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        data = self.grid[self.row][self.col]
        self.row += -1 if self.reverse else 1
        self.col += -1 if self.reverse else 1
        return data

    def has_next(self):
        return ((self.reverse and self.row >= self.row_end) or (not self.reverse and self.row <= self.row_end)) and \
               ((self.reverse and self.col >= self.col_end) or (not self.reverse and self.col <= self.col_end))


class GridMinorDiagonalIterator(GridIterator):
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        """ default: Lower Left -> Upper Right, reverse: Upper Right -> Lower Left """
        if row_end is None:
            row_end = len(grid) - 1 if reverse else 0
        if col_end is None:
            col_end = 0 if reverse else len(grid[0]) - 1
        super().__init__(grid, row_start, col_start, row_end, col_end, reverse)

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        data = self.grid[self.row][self.col]
        self.row += 1 if self.reverse else -1
        self.col += -1 if self.reverse else 1
        return data

    def has_next(self):
        return ((self.reverse and self.row <= self.row_end) or (not self.reverse and self.row >= self.row_end)) and \
               ((self.reverse and self.col >= self.col_end) or (not self.reverse and self.col <= self.col_end))


class GridSpiralIterator(GridIterator):
    def __init__(self,
        grid: list[list],
        row_start: int = 0, col_start: int = 0,
        row_end: int = None, col_end: int = None,
        reverse: bool = False
    ):
        """ default: Clockwise, reverse: Counter-Clockwise """
        super().__init__(grid, row_start, col_start, row_end, col_end, reverse)
        self.row_start, self.col_start = row_start, col_start
        row_margin = min(row_start, len(grid) - 1 - row_start)
        col_margin = min(col_start, len(grid[0]) - 1 - col_start)
        self.is_horizontal = (row_margin <= col_margin)
        self.row_min = self.col_min = min(row_margin, col_margin)
        self.is_upper_row, self.is_left_col = self.row == self.row_min, self.col == self.col_min
        self.row_max, self.col_max = len(grid) - 1 - self.row_min, len(grid[0]) - 1 - self.col_min
        self.has_next = True

    def __next__(self):
        if not self.has_next:
            raise StopIteration
        data = self.grid[self.row][self.col]
        if self.row == self.row_end and self.col == self.col_end:
            self.has_next = False
            return data
        if self.is_horizontal:
            if self.is_upper_row:
                if (self.reverse and self.col > self.col_min) or (not self.reverse and self.col < self.col_max):
                    self.col += -1 if self.reverse else 1
                elif (self.reverse and self.col == self.col_min) or (not self.reverse and self.col == self.col_max):
                    self.row_min += 1 if self.row != self.row_start or self.col != self.col_start else 0
                    self.row += 1
                    self.is_horizontal = not self.is_horizontal
                    self.is_upper_row = not self.is_upper_row
                    self.is_left_col = self.reverse
                else:
                    self.has_next = False
                    raise StopIteration
            else:
                if (self.reverse and self.col < self.col_max) or (not self.reverse and self.col > self.col_min):
                    self.col += 1 if self.reverse else -1
                elif (self.reverse and self.col == self.col_max) or (not self.reverse and self.col == self.col_min):
                    self.row_max -= 1 if self.row != self.row_start or self.col != self.col_start else 0
                    self.row -= 1
                    self.is_horizontal = not self.is_horizontal
                    self.is_upper_row = not self.is_upper_row
                    self.is_left_col = not self.reverse
                else:
                    self.has_next = False
                    raise StopIteration
        else:
            if self.is_left_col:
                if (self.reverse and self.row < self.row_max) or (not self.reverse and self.row > self.row_min):
                    self.row += 1 if self.reverse else -1
                elif (self.reverse and self.row == self.row_max) or (not self.reverse and self.row == self.row_min):
                    self.col += 1 if self.row != self.row_start or self.col != self.col_start else 0
                    self.col_min += 1
                    self.is_horizontal = not self.is_horizontal
                    self.is_upper_row = not self.reverse
                    self.is_left_col = not self.is_left_col
                else:
                    self.has_next = False
                    raise StopIteration
            else:
                if (self.reverse and self.row > self.row_min) or (not self.reverse and self.row < self.row_max):
                    self.row += -1 if self.reverse else 1
                elif (self.reverse and self.row == self.row_min) or (not self.reverse and self.row == self.row_max):
                    self.col -= 1 if self.row != self.row_start or self.col != self.col_start else 0
                    self.col_max -= 1
                    self.is_horizontal = not self.is_horizontal
                    self.is_upper_row = self.reverse
                    self.is_left_col = not self.is_left_col
                else:
                    self.has_next = False
                    raise StopIteration
        return data

    def has_next(self):
        return self.has_next






