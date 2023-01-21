from ezcode.Array.Sub import subarrays_with_target_sum, longest_common_subsequence, longest_common_subarray


def test_longest_common_subsequence():
    assert "BCBA" == "".join(longest_common_subsequence(list("ABCBDAB"), list("BDCABA")))


def test_longest_common_subarray():
    assert "AB" == "".join(longest_common_subarray(list("ABCBDAB"), list("BDCABA")))


def test_subarrays_with_target_sum():
    array = [3, 5, -1, 2, 6, 3, -4, 5, 7, 9, -2, -3, 6]
    assert subarrays_with_target_sum(array, 3) == [(0, 0), (5, 5), (11, 12)]
    assert subarrays_with_target_sum(array, 6) == [(1, 3), (4, 4), (2, 6), (12, 12)]
    assert subarrays_with_target_sum(array, 11) == [(3, 5), (1, 6), (2, 7), (5, 8), (8, 11)]
    assert subarrays_with_target_sum(array, 12) == [(1, 4), (3, 7), (7, 8), (6, 11)]
    assert subarrays_with_target_sum(array, 13) == []
    assert subarrays_with_target_sum(array, 15) == [(0, 4), (1, 5), (6, 10), (5, 11)]
    assert subarrays_with_target_sum(array, 17) == [(4, 8), (6, 9), (8, 12)]
    assert subarrays_with_target_sum(array, 20) == [(5, 9)]
    assert subarrays_with_target_sum(array, 27) == [(2, 9), (1, 11), (4, 12)]

