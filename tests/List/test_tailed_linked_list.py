from collections.abc import MutableSequence
from ezcode.List.LinkedList import LinkedList
from ezcode.List.TailedLinkedList import TailedLinkedList


def test_tailed_linked_list_type():
    assert isinstance(TailedLinkedList(), MutableSequence)
    assert isinstance(TailedLinkedList(), LinkedList)


def test_tailed_linked_list_iterator():
    assert list(TailedLinkedList()) == []
    l = TailedLinkedList([0, 1, 2, 3, 4, 5])
    assert list(l) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]

