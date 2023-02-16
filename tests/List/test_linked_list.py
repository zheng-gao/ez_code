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


def test_linked_list_iterator():
    assert list(iter(LinkedList())) == []
    l = LinkedList([0, 1, 2, 3, 4, 5])
    assert list(iter(l)) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]


def test_linked_list_equal():
    assert LinkedList([]).equal(linked_lists[0])
    assert LinkedList([1]).equal(linked_lists[1])
    assert LinkedList([2, 1]).equal(linked_lists[2])
    assert LinkedList([3, 2, 1]).equal(linked_lists[3])

def test_linked_list_copy():
    assert LinkedList([]).copy().equal(linked_lists[0])
    assert LinkedList([1]).copy().equal(linked_lists[1])
    assert LinkedList([2, 1]).copy().equal(linked_lists[2])
    assert LinkedList([3, 2, 1]).copy().equal(linked_lists[3])

def test_linked_list_reverse():
    assert LinkedList([]).reverse().equal(linked_lists[0])
    assert LinkedList([1]).reverse().equal(linked_lists[1])
    assert LinkedList([2, 1]).reverse().equal(LinkedList([1, 2]))
    assert LinkedList([3, 2, 1]).reverse().equal(LinkedList([1, 2, 3]))


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
    assert list(iter(l)) == [3, 2, 1] 


def test_linked_list_delete_item():
    l = LinkedList([0, 1, 2, 3, 4, 5])
    del l[0]
    del l[2]
    del l[-1]
    assert list(iter(l)) == [1, 2, 4]
    del l[2]
    assert list(iter(l)) == [1, 2]


def test_linked_list_remove_all():
    l = LinkedList([0, 4, 1, 2, 3, 4, 5])
    l.remove_all({2, 3})
    assert list(iter(l)) == [0, 4, 1, 4, 5]
    l.remove_all(4)
    assert list(iter(l)) == [0, 1, 5]


def test_linked_list_append_node():
    l = LinkedList()
    l.append_node(l.new_node(data=0))
    l.append_node(l.new_node(data=1))
    l.append_node(l.new_node(data=2))
    assert list(iter(l)) == [0, 1, 2]


def test_linked_list_extend():
    l = LinkedList()
    l.extend(LinkedList([0, 1, 2]))
    l.extend(LinkedList([3, 4]))
    assert list(iter(l)) == [0, 1, 2, 3, 4]


def test_linked_list_addition():
    l = LinkedList()
    l += LinkedList([0, 1, 2])
    assert list(iter(l)) == [0, 1, 2]
    assert list(iter(l + LinkedList([3, 4]))) == [0, 1, 2, 3, 4]


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
    assert list(iter(l)) == [-100, 7, 0, 1, 9, 2, 3, 6, 4, 5, 8, 100]


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


def test_swap_pairs_of_nodes():
    l = LinkedList()
    l.swap_pairs_of_nodes()
    assert list(iter(l)) == []
    l = LinkedList([0, 1, 2])
    l.swap_pairs_of_nodes()
    assert list(iter(l)) == [0, 2, 1]
    l = LinkedList([0, 1, 2, 3, 4, 5])
    l.swap_pairs_of_nodes()
    assert list(iter(l)) == [1, 0, 3, 2, 5, 4]


# list_0_reverse.head = list_0_reverse.reverse(list_0_reverse.head, list_0_reverse.get_next(list_0_reverse.head))
# list_1_reverse.head = list_1_reverse.reverse(list_1_reverse.head, list_1_reverse.get_next(list_1_reverse.head))
# list_2_reverse.head = list_2_reverse.reverse(list_2_reverse.head, list_2_reverse.get_next(list_2_reverse.head))
# list_3_reverse.head = list_3_reverse.reverse(list_3_reverse.head, list_3_reverse.get_next(list_3_reverse.head))
# assert list_0_copy.equal(list_0_reverse)
# assert list_1_copy.equal(list_1_reverse)
# assert list_2_copy.equal(list_2_reverse)
# assert list_3_copy.equal(list_3_reverse)



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










