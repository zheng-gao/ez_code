from ezcode.Queue.Queue import Queue 


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

