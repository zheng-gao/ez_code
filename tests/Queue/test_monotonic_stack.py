from ezcode.Stack.MonotonicStack import MonotonicStack


def test_monontonic_queue():
    ms = MonotonicStack()  # increasing
    for data, benchmark in zip(
        [5, 3, 1, 2, 4],
        [[5], [3], [1], [2, 1], [4, 2, 1]]
    ):
        ms.push(data)
        assert ms.top(len(ms), always_return_list=True) == benchmark
    ms = MonotonicStack(reverse=True)  # decreasing
    for data, benchmark in zip(
        [5, 3, 1, 2, 4],
        [[5], [3, 5], [1, 3, 5], [2, 3, 5], [4, 5]]
    ):
        ms.push(data)
        assert ms.top(len(ms), always_return_list=True) == benchmark
