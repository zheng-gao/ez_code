from ezcode.List.SinglyLinkedList import SinglyLinkedList


class Node:
    def __init__(self, v=None, n=None):
        self.v = v
        self.n = n

    def __repr__(self):
        return f"Node({self.v})"


def test_singly_linked_list_basics():
    list_0 = SinglyLinkedList(head=None, data_name="v", next_name="n")
    list_0_copy = SinglyLinkedList(head=None, data_name="v", next_name="n")
    list_0_reverse = SinglyLinkedList(head=None, data_name="v", next_name="n")
    list_1 = SinglyLinkedList(head=Node(1), data_name="v", next_name="n")
    list_1_copy = SinglyLinkedList(head=Node(1), data_name="v", next_name="n")
    list_1_reverse = SinglyLinkedList(head=Node(1), data_name="v", next_name="n")
    list_2 = SinglyLinkedList(head=Node(1, Node(2)), data_name="v", next_name="n")
    list_2_copy = SinglyLinkedList(head=Node(1, Node(2)), data_name="v", next_name="n")
    list_2_reverse = SinglyLinkedList(head=Node(2, Node(1)), data_name="v", next_name="n")
    list_3 = SinglyLinkedList(head=Node(1, Node(2, Node(3))), data_name="v", next_name="n")
    list_3_copy = SinglyLinkedList(head=Node(1, Node(2, Node(3))), data_name="v", next_name="n")
    list_3_reverse = SinglyLinkedList(head=Node(3, Node(2, Node(1))), data_name="v", next_name="n")
    assert list_0_copy.equal(list_0)
    assert list_1_copy.equal(list_1)
    assert list_2_copy.equal(list_2)
    assert list_3_copy.equal(list_3)
    assert list_0.copy().equal(list_0_copy)
    assert list_1.copy().equal(list_1_copy)
    assert list_2.copy().equal(list_2_copy)
    assert list_3.copy().equal(list_3_copy)
    assert not list_0.equal(list_1)
    assert not list_1.equal(list_2)
    assert not list_2.equal(list_3)
    assert not list_3.equal(list_0)
    assert str(list_0) == "None"
    assert str(list_1) == "1 ─> None"
    assert str(list_2) == "1 ─> 2 ─> None"
    assert str(list_3) == "1 ─> 2 ─> 3 ─> None"
    assert list_0.to_array() == []
    assert list_1.to_array() == [1]
    assert list_2.to_array() == [1, 2]
    assert list_3.to_array() == [1, 2, 3]
    list_0_reverse_copy = list_0_reverse.copy()
    list_1_reverse_copy = list_1_reverse.copy()
    list_2_reverse_copy = list_2_reverse.copy()
    list_3_reverse_copy = list_3_reverse.copy()
    list_0_reverse_copy.reverse()
    list_1_reverse_copy.reverse()
    list_2_reverse_copy.reverse()
    list_3_reverse_copy.reverse()
    assert list_0_copy.equal(list_0_reverse_copy)
    assert list_1_copy.equal(list_1_reverse_copy)
    assert list_2_copy.equal(list_2_reverse_copy)
    assert list_3_copy.equal(list_3_reverse_copy)
    list_0_reverse.head = list_0_reverse.algorithm.reverse(list_0_reverse.head, list_0_reverse.algorithm.get_next(list_0_reverse.head))
    list_1_reverse.head = list_1_reverse.algorithm.reverse(list_1_reverse.head, list_1_reverse.algorithm.get_next(list_1_reverse.head))
    list_2_reverse.head = list_2_reverse.algorithm.reverse(list_2_reverse.head, list_2_reverse.algorithm.get_next(list_2_reverse.head))
    list_3_reverse.head = list_3_reverse.algorithm.reverse(list_3_reverse.head, list_3_reverse.algorithm.get_next(list_3_reverse.head))
    assert list_0_copy.equal(list_0_reverse)
    assert list_1_copy.equal(list_1_reverse)
    assert list_2_copy.equal(list_2_reverse)
    assert list_3_copy.equal(list_3_reverse)
    try:
        list_0.peek_head() == 0
    except IndexError as e:
        assert e.args[0] == "Peek head at an empty SinglyLinkedList"
    else:
        assert False
    try:
        list_0.pop_head()
    except IndexError as e:
        assert e.args[0] == "Pop head from an empty SinglyLinkedList"
    else:
        assert False
    list_3.delete(set([2, 3]))
    assert list_3.equal(list_1)
    list_2.delete(set([1, 2]))
    assert list_2.equal(list_0)


def test_reverse_sublist():
    lists = [
        SinglyLinkedList(head=Node(0), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1)), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2))), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2, Node(3)))), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4))))), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5)))))), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6))))))), data_name="v", next_name="n"),
        SinglyLinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7)))))))), data_name="v", next_name="n"),
    ]
    for list_orig in lists:
        list_orig.print()
        for i in range(len(list_orig)):
            list_orig_copy = list_orig.copy()
            list_orig_copy.reverse(start_index=i)
            assert list_orig_copy.to_array() == [x for x in range(i)] + [x for x in range(len(list_orig) - 1, i - 1, -1)]
            list_orig_copy = list_orig.copy()
            list_orig_copy.reverse(end_index=i)
            assert list_orig_copy.to_array() == [x for x in range(i, -1, -1)] + [x for x in range(i + 1, len(list_orig))]
            sublist_length = len(list_orig) // 2
            if sublist_length > 0 and i <= len(list_orig) - sublist_length:
                start, end = i, i + sublist_length - 1
                list_orig_copy = list_orig.copy()
                list_orig_copy.reverse(start_index=start, end_index=end)
                assert list_orig_copy.to_array() == [x for x in range(start)] + \
                    [x for x in range(end, start - 1, -1)] + [x for x in range(end + 1, len(list_orig))]


