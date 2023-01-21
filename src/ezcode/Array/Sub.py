

def subarrays_with_target_sum(array: list, target: int) -> list[tuple[int, int]]:
    sum_so_far, sum_occurence, output = 0, {0: [-1]}, list()
    for index_end, data in enumerate(array):
        sum_so_far += data
        sum_matched = sum_so_far - target
        if sum_matched in sum_occurence:
            for index_start in sum_occurence[sum_matched]:
                output.append((index_start + 1, index_end))
        if sum_so_far not in sum_occurence:
            sum_occurence[sum_so_far] = list()
        sum_occurence[sum_so_far].append(index_end)
    return output


def longest_common_subsequence(array_1: list, array_2: list) -> list:
    row_len, col_len = len(array_1) + 1, len(array_2) + 1  # Add one dummy row and one dummy column
    dp = [[0 for _ in range(col_len)] for _ in range(row_len)]
    for row in range(1, row_len):       # skip row = 0
        for col in range(1, col_len):   # skip col = 0
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
    dp = [[0 for _ in range(col_len)] for _ in range(row_len)]
    lcs_size, row_end, lcs = 0, 0, list()
    for row in range(1, row_len):
        for col in range(1, col_len):
            if array_1[row - 1] == array_2[col - 1]:  # else dp[row][col] = 0 (initial value)
                dp[row][col] = dp[row - 1][col - 1] + 1
                if dp[row][col] > lcs_size:
                    lcs_size, row_end = dp[row][col], row
    while lcs_size > 0:
        lcs.append(array_1[row_end - 1])
        row_end, lcs_size = row_end - 1, lcs_size - 1
    return lcs[::-1]


