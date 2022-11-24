from ezcode.queue import Queue, MonotonicQueue


def test_queue():
    queue = Queue()
    for i in range(3):
        assert len(queue) == i
        queue.push(i)
        assert queue.top() == 0
    assert queue.top(k=2) == [0, 1]
    assert queue.top(k=3) == [0, 1, 2]
    for i in range(3):
        assert len(queue) == 3 - i
        assert queue.top() == i
        assert queue.pop() == i


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
