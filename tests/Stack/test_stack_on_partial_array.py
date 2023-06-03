from ezcode.Stack.StackOnPartialArray import StackOnPartialArray


def test_stack_on_partial_array():
    array = ["X"] * 10
    stack = StackOnPartialArray(array=array, start=3, end=8)
    for x in range(5):
        stack.push(x)
    assert array == ["X", "X", "X", 0, 1, 2, 3, 4, "X", "X"]
    for x in range(4, 0, -1):
        assert stack.top() == x
        assert stack.pop() == x
    for x in range(5):
        stack.push(x)
    assert array == ["X", "X", "X", 0, 0, 1, 2, 3, 4, "X"]
    assert stack.top() == 4
    assert stack.top(k=6) == [4, 3, 2, 1, 0, 0]
