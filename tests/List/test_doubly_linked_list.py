from collections.abc import MutableSequence
from ezcode.List.LinkedList import LinkedList
from ezcode.List.TailedLinkedList import TailedLinkedList
from ezcode.List.DoublyLinkedList import DoublyLinkedList


def test_doubly_linked_list_type():
    assert isinstance(DoublyLinkedList(), MutableSequence)
    assert isinstance(DoublyLinkedList(), LinkedList)
    assert isinstance(DoublyLinkedList(), TailedLinkedList)
    

def test_doubly_linked_list_iterator():
    assert list(DoublyLinkedList()) == []
    l = DoublyLinkedList([0, 1, 2, 3, 4, 5])
    assert list(l) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]
