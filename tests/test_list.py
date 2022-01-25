from ezcode.list.stack import Stack
from ezcode.list.queue import Queue
from fixture.list import s_list, s_list_copied, s_list_reversed


def test_print():
    pass


def test_is_copied():
    assert s_list.is_copied(s_list_copied)


def test_copy():
    assert s_list.copy().is_copied(s_list_copied)
    assert not s_list.is_copied(s_list_reversed)


def test_reverse():
    reversed_list = s_list.copy()
    reversed_list.reverse()
    assert reversed_list.is_copied(s_list_reversed)


def test_queue():
    queue = Queue()
    for i in range(3):
        assert len(queue) == i
        queue.push(i)
        assert queue.peek() == 0
    for i in range(3):
        assert len(queue) == 3 - i
        assert queue.peek() == i
        assert queue.pop() == i


def test_stack():
    stack = Stack()
    for i in range(3):
        assert len(stack) == i
        stack.push(i)
        assert stack.peek() == i
    for i in range(3):
        assert len(stack) == 3 - i
        assert stack.peek() == 2 - i
        assert stack.pop() == 2 - i
