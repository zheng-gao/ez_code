import math

from typing import Callable


class SparseTable:
    """
        Offline
        Preprocess Time: O(NlogN)
        Range Query Time: O(1)
        Space: O(NlogN)
    """
    def __init__(self, merge: Callable = max, data_list: list = None):
        self.merge = merge  # min/max only, not work for sum, since the sub-queries are overlapped
        self.dp = None
        if data_list is not None:
            self.build_table(data_list=data_list)

    def build_table(self, data_list: list):
        """
            Time: O(NlogN), Space: O(NlogN)
            dp[i][j] = merge(data_list[i:pow(2,j)]) = merge(dp[i][j-1], dp[i+pow(2,j-1)][j-1])
            e.g. data_list = [3, 2, 4, 5, 6, 8, 1, 9, 7, 0], merge = min
            dp = [
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
        """
        row_len = len(data_list)
        col_len = math.ceil(math.log(row_len, 2))
        init_value = float("inf") if self.merge == min else float("-inf")
        self.dp = [[init_value] * col_len for _ in range(row_len)]
        for row, data in enumerate(data_list):
            self.dp[row][0] = data
        for col in range(1, col_len):  # loop col first since new_row might not be available
            for row in range(0, row_len):
                new_row = row + (1 << (col - 1))
                if new_row >= row_len:
                    break
                self.dp[row][col] = self.merge(self.dp[row][col - 1], self.dp[new_row][col - 1])

    def rmq(self, begin: int, end: int):
        """
            RMQ: Range Maximum(Minimum) Query
            Time: O(1), Space: O(1)
            data_list[begin:pow(2,k)] and data_list[end - pow(2,k) + 1:pow(2,k)] should cover data_list[begin:end + 1] with overlapping
            e.g. data_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            rmq(2, 6), k = 2, dp[2][2] = [2, 3, 4, 5], dp[3][2] = [3, 4, 5, 6], merge = [2, 3, 4, 5, 6]
            rmq(2, 8), k = 2, dp[2][2] = [2, 3, 4, 5], dp[5][2] = [5, 6, 7, 8], merge = [2, 3, 4, 5, 6, 7, 8]
        """
        if end < begin:
            raise ValueError(f"end({end}) < begin({begin})")
        k = math.floor(math.log(end - begin + 1, 2))
        return self.merge(self.dp[begin][k], self.dp[end - (1 << k) + 1][k])
