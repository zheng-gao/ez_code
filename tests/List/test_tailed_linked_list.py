from ezcode.List.TailedLinkedList import TailedLinkedList


def test_linked_list_iterator():
    assert list(iter(TailedLinkedList())) == []
    l = TailedLinkedList([0, 1, 2, 3, 4, 5])
    assert list(iter(l)) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]

