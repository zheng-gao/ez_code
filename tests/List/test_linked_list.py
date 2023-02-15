from ezcode.List.LinkedList import LinkedList


class Node:
    def __init__(self, v=None, n=None):
        self.v = v
        self.n = n


linked_lists = [
    LinkedList(head=None, data_name="v", next_name="n"),
    LinkedList(head=Node(1), data_name="v", next_name="n"),
    LinkedList(head=Node(1, Node(2)), data_name="v", next_name="n"),
    LinkedList(head=Node(1, Node(2, Node(3))), data_name="v", next_name="n")
]


def test_linkedin_list_printer():
    assert str(linked_lists[0]) == "None (H)"
    assert str(linked_lists[1]) == "None <─ 1 (H)"
    assert str(linked_lists[2]) == "None <─ 2 <─ 1 (H)"
    assert str(linked_lists[3]) == "None <─ 3 <─ 2 <─ 1 (H)"
    assert linked_lists[0].to_string(include_end=False) == "(H)"
    assert linked_lists[1].to_string(include_end=False) == "1 (H)"
    assert linked_lists[2].to_string(include_end=False) == "2 <─ 1 (H)"
    assert linked_lists[3].to_string(include_end=False) == "3 <─ 2 <─ 1 (H)"
    assert linked_lists[0].to_string(mark_head=False, include_end=False) == ""
    assert linked_lists[1].to_string(mark_head=False, include_end=False) == "1"
    assert linked_lists[2].to_string(mark_head=False, include_end=False) == "2 <─ 1"
    assert linked_lists[3].to_string(mark_head=False, include_end=False) == "3 <─ 2 <─ 1"
    assert linked_lists[0].to_string(reverse=True) == "(H) None"
    assert linked_lists[1].to_string(reverse=True) == "(H) 1 ─> None"
    assert linked_lists[2].to_string(reverse=True) == "(H) 1 ─> 2 ─> None"
    assert linked_lists[3].to_string(reverse=True) == "(H) 1 ─> 2 ─> 3 ─> None"
    assert linked_lists[0].to_string(reverse=True, mark_head=False) == "None"
    assert linked_lists[1].to_string(reverse=True, mark_head=False) == "1 ─> None"
    assert linked_lists[2].to_string(reverse=True, mark_head=False) == "1 ─> 2 ─> None"
    assert linked_lists[3].to_string(reverse=True, mark_head=False) == "1 ─> 2 ─> 3 ─> None"
    assert linked_lists[0].to_string(reverse=True, mark_head=False, include_end=False) == ""
    assert linked_lists[1].to_string(reverse=True, mark_head=False, include_end=False) == "1"
    assert linked_lists[2].to_string(reverse=True, mark_head=False, include_end=False) == "1 ─> 2"
    assert linked_lists[3].to_string(reverse=True, mark_head=False, include_end=False) == "1 ─> 2 ─> 3"
    assert linked_lists[0].to_string(reverse=True, include_end=False) == "(H)"
    assert linked_lists[1].to_string(reverse=True, include_end=False) == "(H) 1"
    assert linked_lists[2].to_string(reverse=True, include_end=False) == "(H) 1 ─> 2"
    assert linked_lists[3].to_string(reverse=True, include_end=False) == "(H) 1 ─> 2 ─> 3"


def test_linked_list_equal():
    linked_list = LinkedList([])
    assert linked_list.equal(linked_lists[0])
    for index, data in enumerate([1, 2, 3], start=1):
        linked_list.append(data)
        assert linked_list.equal(linked_lists[index])


def test_linked_list_iterator():
    l = LinkedList([0, 1, 2, 3, 4, 5])
    assert list(iter(l)) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]
    del l[0]
    del l[2]
    del l[-1]
    assert list(iter(l)) == [1, 2, 4]
    del l[2]
    assert list(iter(l)) == [1, 2]


def test_linked_list_cycle_detection():
    n = [Node(0), Node(1), Node(1), Node(3), Node(4), Node(5), Node(6), Node(7)]
    for i in range(len(n) - 1):
        n[i].n = n[i + 1]
    n[-1].n = n[2]
    assert LinkedList(data_name="v", next_name="n").has_cycle(n[0])
    assert LinkedList(data_name="v", next_name="n").get_cycle_entrance(n[0]) == n[2]


def test_linked_list_basics():
    list_0 = LinkedList(head=None, data_name="v", next_name="n")
    list_0_copy = LinkedList(head=None, data_name="v", next_name="n")
    list_0_reverse = LinkedList(head=None, data_name="v", next_name="n")
    list_1 = LinkedList(head=Node(1), data_name="v", next_name="n")
    list_1_copy = LinkedList(head=Node(1), data_name="v", next_name="n")
    list_1_reverse = LinkedList(head=Node(1), data_name="v", next_name="n")
    list_2 = LinkedList(head=Node(1, Node(2)), data_name="v", next_name="n")
    list_2_copy = LinkedList(head=Node(1, Node(2)), data_name="v", next_name="n")
    list_2_reverse = LinkedList(head=Node(2, Node(1)), data_name="v", next_name="n")
    list_3 = LinkedList(head=Node(1, Node(2, Node(3))), data_name="v", next_name="n")
    list_3_copy = LinkedList(head=Node(1, Node(2, Node(3))), data_name="v", next_name="n")
    list_3_reverse = LinkedList(head=Node(3, Node(2, Node(1))), data_name="v", next_name="n")
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
    assert list(iter(list_0)) == []
    assert list(iter(list_1)) == [1]
    assert list(iter(list_2)) == [2, 1]
    assert list(iter(list_3)) == [3, 2, 1]
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
    # list_0_reverse.head = list_0_reverse.reverse(list_0_reverse.head, list_0_reverse.get_next(list_0_reverse.head))
    # list_1_reverse.head = list_1_reverse.reverse(list_1_reverse.head, list_1_reverse.get_next(list_1_reverse.head))
    # list_2_reverse.head = list_2_reverse.reverse(list_2_reverse.head, list_2_reverse.get_next(list_2_reverse.head))
    # list_3_reverse.head = list_3_reverse.reverse(list_3_reverse.head, list_3_reverse.get_next(list_3_reverse.head))
    # assert list_0_copy.equal(list_0_reverse)
    # assert list_1_copy.equal(list_1_reverse)
    # assert list_2_copy.equal(list_2_reverse)
    # assert list_3_copy.equal(list_3_reverse)
    try:
        list_0[-1] == 0
    except IndexError as e:
        assert e.args[0] == "list index -1 out of range"
    else:
        assert False
    try:
        list_0.pop()
    except KeyError as e:
        assert e.args[0] == "Pop from empty list"
    else:
        assert False
    list_3.remove_all(set([2, 3]))
    assert list_3.equal(list_1)
    list_2.remove_all(set([1, 2]))
    assert list_2.equal(list_0)


# def test_reverse_sublist():
#     lists = [
#         LinkedList(head=Node(0), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1)), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2))), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2, Node(3)))), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4))))), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5)))))), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6))))))), data_name="v", next_name="n"),
#         LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7)))))))), data_name="v", next_name="n"),
#     ]
#     for list_orig in lists:
#         list_orig.print()
#         for i in range(len(list_orig)):
#             list_orig_copy = list_orig.copy()
#             list_orig_copy.reverse(start_index=i)
#             assert list_orig_copy.to_array() == [x for x in range(i)] + [x for x in range(len(list_orig) - 1, i - 1, -1)]
#             list_orig_copy = list_orig.copy()
#             list_orig_copy.reverse(end_index=i)
#             assert list_orig_copy.to_array() == [x for x in range(i, -1, -1)] + [x for x in range(i + 1, len(list_orig))]
#             sublist_length = len(list_orig) // 2
#             if sublist_length > 0 and i <= len(list_orig) - sublist_length:
#                 start, end = i, i + sublist_length - 1
#                 list_orig_copy = list_orig.copy()
#                 list_orig_copy.reverse(start_index=start, end_index=end)
#                 assert list_orig_copy.to_array() == [x for x in range(start)] + \
#                     [x for x in range(end, start - 1, -1)] + [x for x in range(end + 1, len(list_orig))]










