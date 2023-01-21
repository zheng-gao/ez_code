from ezcode.Queue.MonotonicQueue import MonotonicQueue


def test_monontonic_queue():
    mq = MonotonicQueue(is_increasing=True)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 3, 1, 1, 1]):
        mq.push(data)
        assert mq.top() == benchmark
    assert mq.top(k=3) == [1, 2, 4]
    mq = MonotonicQueue(is_increasing=False)
    for data, benchmark in zip([5, 3, 1, 2, 4], [5, 5, 5, 5, 5]):
        mq.push(data)
        assert mq.top() == benchmark
    assert mq.top(k=2) == [5, 4]
