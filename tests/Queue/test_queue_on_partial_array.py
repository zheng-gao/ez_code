from ezcode.Queue.QueueOnPartialArray import QueueOnPartialArray


def test_queue_on_partial_array():
    array = ["X"] * 10
    queue = QueueOnPartialArray(array=array, start=3, end=8)
    for x in range(5):
        queue.push(x)
    assert array == ["X", "X", "X", 0, 1, 2, 3, 4, "X", "X"]
    for x in range(4):
        assert queue.top() == x
        assert queue.pop() == x
    for x in range(4):
        queue.push(x)
    assert array == ["X", "X", "X", 1, 2, 3, 3, 4, 0, "X"]
    assert queue.top() == 4
    assert queue.top(k=4) == [4, 0, 1, 2]
