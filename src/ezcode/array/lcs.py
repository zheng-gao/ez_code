from ezcode.array.matrix import init_matrix


def longest_common_subsequence(array_1: list, array_2: list) -> list:
    row_len, col_len = len(array_1) + 1, len(array_2) + 1  # Add one dummy row and one dummy column
    dp = init_matrix(row=row_len, col=col_len, init=0)
    for row in range(1, row_len):
        for col in range(1, col_len):
            dp[row][col] = dp[row - 1][col - 1] + 1 if array_1[row - 1] == array_2[col - 1] else max(dp[row - 1][col], dp[row][col - 1])
    row, col, lcs = row_len - 1, col_len - 1, list()
    while row > 0 and col > 0:
        if array_1[row - 1] == array_2[col - 1]:
            lcs.append(array_1[row - 1])
            row, col = row - 1, col - 1
        else:
            row, col = (row - 1, col) if dp[row - 1][col] >= dp[row][col - 1] else (row, col - 1)
    return lcs[::-1]


def longest_common_subarray(array_1: list, array_2: list) -> list:
    row_len, col_len = len(array_1) + 1, len(array_2) + 1  # Add one dummy row and one dummy column
    dp = init_matrix(row=row_len, col=col_len, init=0)
    lcs_size, row_end = 0, 0
    for row in range(1, row_len):
        for col in range(1, col_len):
            if array_1[row - 1] == array_2[col - 1]:
                dp[row][col] = dp[row - 1][col - 1] + 1
                if dp[row][col] > lcs_size:
                    lcs_size, row_end = dp[row][col], row
    lcs = list()
    while lcs_size > 0:
        lcs.append(array_1[row_end - 1])
        row_end -= 1
        lcs_size -= 1
    return lcs[::-1]
