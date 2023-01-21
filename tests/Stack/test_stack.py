from ezcode.Stack.Stack import Stack
from ezcode.Stack.MinMaxStack import MinMaxStack
from ezcode.Stack.PersistentStack import PersistentStack


def test_stack():
    stack = Stack()
    for i in range(3):
        assert len(stack) == i
        stack.push(i)
        assert stack.top() == i
    assert stack.top(k=2) == [2, 1]
    assert stack.top(k=3) == [2, 1, 0]
    for i in range(3):
        assert len(stack) == 3 - i
        assert stack.top() == 2 - i
        assert stack.pop() == 2 - i


def test_min_max_stack():
    min_max_stack = MinMaxStack()
    for data, min_data, max_data in zip([2, 1, 3, 5, 4], [2, 1, 1, 1, 1], [2, 2, 3, 5, 5]):
        min_max_stack.push(data)
        assert min_max_stack.get_min() == min_data
        assert min_max_stack.get_max() == max_data
    for min_data, max_data in zip([1, 1, 1, 2], [5, 3, 2, 2]):
        min_max_stack.pop()
        assert min_max_stack.get_min() == min_data
        assert min_max_stack.get_max() == max_data


def test_persistent_stack():
    stacks = [PersistentStack()]
    stacks.append(stacks[-1].push(1))
    stacks.append(stacks[-1].push(2))
    stacks.append(stacks[-1].push(3))
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].push(4))
    stacks.append(stacks[-1].push(5))
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].push(6))
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].push(7))
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].pop())
    stacks.append(stacks[-1].pop())
    benchmarks = [
        [],
        [1],
        [1, 2],
        [1, 2, 3],
        [1, 2],
        [1, 2, 4],
        [1, 2, 4, 5],
        [1, 2, 4],
        [1, 2, 4, 6],
        [1, 2, 4],
        [1, 2],
        [1, 2, 7],
        [1, 2],
        [1],
        []
    ]
    for s, b in zip(stacks, benchmarks):
        assert list(s) == b
        assert len(s) == len(b)
    assert stacks[1].top() == 1
    assert stacks[5].top(k=1) == 4
    assert stacks[6].top(k=3) == [5, 4, 2]
    assert stacks[8].top(k=3) == [6, 4, 2]


