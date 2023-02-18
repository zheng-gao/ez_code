from ezcode.List.DoublyLinkedList import DoublyLinkedList


def test_linked_list_iterator():
    assert list(iter(DoublyLinkedList())) == []
    l = DoublyLinkedList([0, 1, 2, 3, 4, 5])
    assert list(iter(l)) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]
