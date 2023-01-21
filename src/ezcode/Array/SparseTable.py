from math import ceil, floor, log
from typing import Callable

from ezcode.Array.Utils import validate_index_range


class SparseTable:
    """
                            Sparse Table      Segment Tree
        Data            :   No Data Update    Can Update Data, No Data Insert/Delete
        Merge           :   Min/Max Only      Min, Max, Sum, ... lambda x,y
        Space           :   O(NlogN)          O(N)
        Preprocess Time :   O(NlogN)          O(N)
        Range Query Time:   O(1)              O(logN)
    """
    def __init__(self, merge: Callable = max, data_list: list = None):
        if merge not in [min, max]:
            raise NotImplementedError("Only support min/max")  # not work for sum, since the sub-queries are overlapped
        self.merge = merge
        self.dp_table = None
        if data_list is not None:
            self.build_table(data_list=data_list)

    def build_table(self, data_list: list):
        """
            Time: O(NlogN), Space: O(NlogN)
            dp_table[i][j] = merge(data_list[i:i+2^j+1]) = merge(dp_table[i][j-1], dp_table[i+2^(j-1)][j-1])
            e.g. data_list = [3, 2, 4, 5, 6, 8, 1, 9, 7, 0], merge = min
            dp_table = [
                [  3,   2,   2,   1],
                [  2,   2,   2,   1],
                [  4,   4,   4,   0],
                [  5,   5,   1,   1],
                [  6,   6,   1,   1],
                [  8,   1,   1,   1],
                [  1,   1,   0, inf],
                [  9,   7,   7, inf],
                [  7,   0, inf, inf],
                [  0, inf, inf, inf],
            ]

            The first column is data_list where j=0, dp_table[i][0] = data_list[i]
            j=1, dp_table[i][1] = merge(dp_table[i][0], dp_table[i+1][0])  -> cover data_list[i:i+2]
            j=2, dp_table[i][2] = merge(dp_table[i][1], dp_table[i+2][1])  -> cover data_list[i:i+4]
            j=3, dp_table[i][3] = merge(dp_table[i][2], dp_table[i+4][2])  -> cover data_list[i:i+8]
            ...
        """
        row_len = len(data_list)
        col_len = ceil(log(row_len, 2))  # row_len = 10, col_len = 4
        init_value = float("inf") if self.merge == min else float("-inf")
        self.dp_table = [[init_value] * col_len for _ in range(row_len)]
        for row, data in enumerate(data_list):
            self.dp_table[row][0] = data
        for col in range(1, col_len):  # loop col first since new_row might not be available
            for row in range(0, row_len):
                new_row = row + (1 << (col - 1))
                if new_row >= row_len:
                    break
                self.dp_table[row][col] = self.merge(self.dp_table[row][col - 1], self.dp_table[new_row][col - 1])

    def range_query(self, start: int, end: int):
        """
            RMQ: Range Maximum(Minimum) Query
            Time: O(1), Space: O(1)
            data_list[start:2^k] and data_list[end+1-2^k:2^k] should cover data_list[start:end+1] with overlapping
            e.g. data_list = [3, 2, 4, 5, 6, 8, 1, 9, 7, 0]
            query(2, 6), k = 2:
                 left = dp_table[2][2] covers [4, 5, 6, 8]
                right = dp_table[3][2] covers [5, 6, 8, 1]
                merge covers [4, 5, 6, 8, 1,]
            query(2, 9), k = 3:
                 left = dp_table[2][3] covers [4, 5, 6, 8, 1, 9, 7, 0]
                right = dp_table[2][3] = left
                merge covers [4, 5, 6, 8, 1, 9, 7, 0]
        """
        validate_index_range(start, end, 0, len(self.dp_table) - 1)
        k = floor(log(end - start + 1, 2))
        return self.merge(self.dp_table[start][k], self.dp_table[end + 1 - (1 << k)][k])





