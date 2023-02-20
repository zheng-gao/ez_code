from collections.abc import MutableSequence
from ezcode.List.LinkedList import LinkedList


class Node:
    def __init__(self, v=None, n=None):
        self.v = v
        self.n = n


linked_lists = [
    LinkedList(head=None, data_name="v", next_name="n"),
    LinkedList(head=Node(0), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1)), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1, Node(2))), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4))))), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5)))))), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6))))))), data_name="v", next_name="n"),
    LinkedList(head=Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7)))))))), data_name="v", next_name="n"),
]


def test_linked_list_type():
    assert isinstance(LinkedList(), MutableSequence)


def test_linkedin_list_printer():
    assert str(linked_lists[0]) == "None (H)"
    assert str(linked_lists[1]) == "None <─ 0 (H)"
    assert str(linked_lists[2]) == "None <─ 1 <─ 0 (H)"
    assert str(linked_lists[3]) == "None <─ 2 <─ 1 <─ 0 (H)"
    assert linked_lists[0].to_string(include_end=False) == "(H)"
    assert linked_lists[1].to_string(include_end=False) == "0 (H)"
    assert linked_lists[2].to_string(include_end=False) == "1 <─ 0 (H)"
    assert linked_lists[3].to_string(include_end=False) == "2 <─ 1 <─ 0 (H)"
    assert linked_lists[0].to_string(mark_head=False, include_end=False) == ""
    assert linked_lists[1].to_string(mark_head=False, include_end=False) == "0"
    assert linked_lists[2].to_string(mark_head=False, include_end=False) == "1 <─ 0"
    assert linked_lists[3].to_string(mark_head=False, include_end=False) == "2 <─ 1 <─ 0"
    assert linked_lists[0].to_string(reverse=True) == "(H) None"
    assert linked_lists[1].to_string(reverse=True) == "(H) 0 ─> None"
    assert linked_lists[2].to_string(reverse=True) == "(H) 0 ─> 1 ─> None"
    assert linked_lists[3].to_string(reverse=True) == "(H) 0 ─> 1 ─> 2 ─> None"
    assert linked_lists[0].to_string(reverse=True, mark_head=False) == "None"
    assert linked_lists[1].to_string(reverse=True, mark_head=False) == "0 ─> None"
    assert linked_lists[2].to_string(reverse=True, mark_head=False) == "0 ─> 1 ─> None"
    assert linked_lists[3].to_string(reverse=True, mark_head=False) == "0 ─> 1 ─> 2 ─> None"
    assert linked_lists[0].to_string(reverse=True, mark_head=False, include_end=False) == ""
    assert linked_lists[1].to_string(reverse=True, mark_head=False, include_end=False) == "0"
    assert linked_lists[2].to_string(reverse=True, mark_head=False, include_end=False) == "0 ─> 1"
    assert linked_lists[3].to_string(reverse=True, mark_head=False, include_end=False) == "0 ─> 1 ─> 2"
    assert linked_lists[0].to_string(reverse=True, include_end=False) == "(H)"
    assert linked_lists[1].to_string(reverse=True, include_end=False) == "(H) 0"
    assert linked_lists[2].to_string(reverse=True, include_end=False) == "(H) 0 ─> 1"
    assert linked_lists[3].to_string(reverse=True, include_end=False) == "(H) 0 ─> 1 ─> 2"


def test_linked_list_iterator():
    assert list(LinkedList()) == []
    l = LinkedList([0, 1, 2, 3, 4, 5])
    assert list(l) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]


def test_linked_list_equal():
    assert LinkedList([]).equal(linked_lists[0])
    assert LinkedList([0]).equal(linked_lists[1])
    assert LinkedList([1, 0]).equal(linked_lists[2])
    assert LinkedList([2, 1, 0]).equal(linked_lists[3])


def test_linked_list_copy():
    assert LinkedList([]).copy().equal(linked_lists[0])
    assert LinkedList([0]).copy().equal(linked_lists[1])
    assert LinkedList([1, 0]).copy().equal(linked_lists[2])
    assert LinkedList([2, 1, 0]).copy().equal(linked_lists[3])


def test_linked_list_reverse():
    assert list(LinkedList().reverse()) == []
    assert list(LinkedList([0]).reverse()) == [0]
    assert list(LinkedList([0, 1]).reverse()) == [1, 0]
    assert list(LinkedList([0, 1, 2]).reverse()) == [2, 1, 0]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(4, 5)) == [0, 1, 2, 3, 5, 4]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(2, 5)) == [0, 1, 5, 4, 3, 2]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(0, 1)) == [1, 0, 2, 3, 4, 5]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(0, 3)) == [3, 2, 1, 0, 4, 5]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(2, 4)) == [0, 1, 4, 3, 2, 5]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(1, 4)) == [0, 4, 3, 2, 1, 5]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(0, 5)) == [5, 4, 3, 2, 1, 0]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(2, 3)) == [0, 1, 3, 2, 4, 5]
    assert list(LinkedList([0, 1, 2, 3, 4, 5]).reverse(2, 2)) == [0, 1, 2, 3, 4, 5]  # No change
    for list_orig in linked_lists:
        for i in range(len(list_orig)):
            list_orig_copy = list_orig.copy()
            list_orig_copy.reverse(start=i)
            assert list(list_orig_copy) == \
                list(range(len(list_orig) - 1, len(list_orig) - 1 - i, -1)) + \
                list(range(len(list_orig) - i))
            list_orig_copy = list_orig.copy()
            list_orig_copy.reverse(end=i)
            assert list(list_orig_copy) == \
                list(range(len(list_orig) - 1 - i, len(list_orig))) + \
                list(range(len(list_orig) - 2 - i, -1, -1))
            sublist_length = len(list_orig) // 2
            if sublist_length > 0 and i <= len(list_orig) - sublist_length:
                start, end = i, i + sublist_length - 1
                list_orig_copy = list_orig.copy()
                list_orig_copy.reverse(start=start, end=end)
                assert list(list_orig_copy) == \
                    list(range(len(list_orig) - 1, len(list_orig) - 1 - start, -1)) + \
                    list(range(len(list_orig) - 1 - end, len(list_orig) - start)) + \
                    list(range(len(list_orig) - 2 - end, -1, -1))
    assert list(LinkedList().reverse(group_size=1)) == []
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(1, 8, 3, remainder_on_left=True)) == [0, 2, 1, 5, 4, 3, 8, 7, 6, 9]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(1, group_size=3, remainder_on_left=True)) == [0, 3, 2, 1, 6, 5, 4, 9, 8, 7]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(group_size=7, remainder_on_left=True)) == [2, 1, 0, 9, 8, 7, 6, 5, 4, 3]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(0, -1, 2, remainder_on_left=True)) == [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8]).reverse(end=-1, group_size=2, remainder_on_left=True)) == [0, 2, 1, 4, 3, 6, 5, 8, 7]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(4, 8, 1)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # No change
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(1, 8, 3, remainder_on_left=False)) == [0, 3, 2, 1, 6, 5, 4, 8, 7, 9]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(2, group_size=3, remainder_on_left=False)) == [0, 1, 4, 3, 2, 7, 6, 5, 9, 8]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reverse(group_size=7, remainder_on_left=False)) == [6, 5, 4, 3, 2, 1, 0, 9, 8, 7]
    assert list(LinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8]).reverse(end=-1, group_size=2, remainder_on_left=False)) == [1, 0, 3, 2, 5, 4, 7, 6, 8]


def test_linked_list_get_item():
    l = LinkedList([0, 1, 2])
    for i in [0, 1, 2]:
        assert l[i] == i
    for i in [-1, -2, -3]:
        assert l[i] == len(l) + i


def test_linked_list_set_item():
    l = LinkedList([0, 1, 2])
    l[0] = 3
    l[-1] = 1
    l[1] = 2
    assert list(l) == [3, 2, 1] 


def test_linked_list_delete_item():
    l = LinkedList([0, 1, 2, 3, 4, 5])
    del l[0]
    del l[2]
    del l[-1]
    assert list(l) == [1, 2, 4]
    del l[2]
    assert list(l) == [1, 2]


def test_linked_list_remove_all():
    l = LinkedList([0, 4, 1, 2, 3, 4, 5])
    l.remove_all({2, 3})
    assert list(l) == [0, 4, 1, 4, 5]
    l.remove_all(4)
    assert list(l) == [0, 1, 5]


def test_linked_list_append_node():
    l = LinkedList()
    l.append_node(l.new_node(data=0))
    l.append_node(l.new_node(data=1))
    l.append_node(l.new_node(data=2))
    assert list(l) == [0, 1, 2]


def test_linked_list_extend():
    l = LinkedList()
    l.extend(LinkedList([0, 1, 2]))
    l.extend(LinkedList([3, 4]))
    assert list(l) == [0, 1, 2, 3, 4]


def test_linked_list_addition():
    l = LinkedList()
    l += LinkedList([0, 1, 2])
    assert list(l) == [0, 1, 2]
    assert list(l + LinkedList([3, 4])) == [0, 1, 2, 3, 4]


def test_linked_list_pop():
    l = LinkedList([0, 1, 2, 3, 4, 5])
    for i in range(5, -1, -1):
        assert l.pop() == i


def test_linked_list_insert():
    l = LinkedList([0, 1, 2, 3, 4, 5])
    l.insert(index=2, data=9)
    l.insert(index=0, data=7)
    l.insert(index=-1, data=8)
    l.insert(index=-3, data=6)
    l.insert(index=-100, data=-100)
    l.insert(index=100, data=100)
    assert list(l) == [-100, 7, 0, 1, 9, 2, 3, 6, 4, 5, 8, 100]


def test_linked_list_exception():
    try:
        LinkedList()[-1] = 0
    except IndexError as e:
        assert e.args[0] == "list index -1 out of range"
    else:
        assert False
    try:
        LinkedList([0, 1, 2])[3] = 0
    except IndexError as e:
        assert e.args[0] == "list index 3 out of range"
    else:
        assert False
    try:
        LinkedList().pop()
    except KeyError as e:
        assert e.args[0] == "Pop from empty list"
    else:
        assert False


def test_linked_list_cycle_detection():
    n = [Node(0), Node(1), Node(1), Node(3), Node(4), Node(5), Node(6), Node(7)]
    for i in range(len(n) - 1):
        n[i].n = n[i + 1]
    n[-1].n = n[2]
    assert LinkedList(data_name="v", next_name="n").has_cycle(n[0])
    assert LinkedList(data_name="v", next_name="n").get_cycle_entrance(n[0]) == n[2]


def test_get_intersection_node():
    long_head = Node("L1", Node("L2", Node("L3", Node("L4", Node("L5")))))
    short_head = Node("S1", long_head.n.n.n)
    long_list = LinkedList(head=long_head, data_name="v", next_name="n")
    short_list = LinkedList(head=short_head, data_name="v", next_name="n")
    assert short_list.get_intersection_node(long_list).v == "L4"
    assert long_list.get_intersection_node(short_list).v == "L4"
    other_list = LinkedList(head=Node("S1", Node("S2")), data_name="v", next_name="n")
    assert long_list.get_intersection_node(other_list) is None












