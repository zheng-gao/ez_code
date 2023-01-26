from ezcode.Tree.AVLTree import AVLTree
from ezcode.Tree.RedBlackTree import RedBlackTree
from ezcode.Set.TreeSet import TreeSet


def test_tree_set_add_and_update_item():
    def _test(tree):
        ts = TreeSet([5, 3, 8, 9, 0, 1, 6, 4, 2, 7], tree)
        assert list(ts) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert list(reversed(ts)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9][::-1]
        ts.add(1)
        ts.add(8)
        assert list(ts) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert list(reversed(ts)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9][::-1]
        ts.update([7, 6, -2, -3, -1])
        assert list(ts) == [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert list(reversed(ts)) == [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9][::-1]

    _test(AVLTree())
    _test(RedBlackTree())


def test_tree_set_remove_item():
    def _test(tree):
        ts = TreeSet([2, 3, 0, 9, 8, 1, 7, 4, 5, 6], tree)
        ts.remove(3)
        ts.remove(7)
        assert list(ts) == [0, 1, 2, 4, 5, 6, 8, 9]
        assert list(reversed(ts)) == [0, 1, 2, 4, 5, 6, 8, 9][::-1]
        ts.remove(3)
        ts.remove(5)
        ts.remove(0)
        ts.remove(9)
        assert list(ts) == [1, 2, 4, 6, 8]
        assert list(reversed(ts)) == [1, 2, 4, 6, 8][::-1]
        ts.clear()
        assert list(ts) == []

    _test(AVLTree())
    _test(RedBlackTree())


def test_tree_set_contains():
    def _test(tree):
        ts = TreeSet([6, 9, 8, 3, 2, 1, 5, 0, 4, 7], tree)
        assert 5 in ts
        assert 8 in ts
        assert 10 not in ts
        ts.remove(4)
        assert 4 not in ts
        ts.remove(5)
        assert 5 not in ts

    _test(AVLTree())
    _test(RedBlackTree())


def test_tree_set_pop():
    def _test(tree):
        ts = TreeSet([6, 8, 9, 3, 2, 1, 7, 5, 0, 4], tree)
        for i in range(len(ts)):
            i = ts.pop()
        ts = TreeSet([7, 8, 6, 1, 2, 4, 5, 9, 0, 3], tree)
        for i in range(len(ts) - 1, -1, -1):
            i = ts.pop(reverse=True)

    _test(AVLTree())
    _test(RedBlackTree())


