from collections.abc import MutableSequence
from ezcode.List.LinkedList import LinkedList
from ezcode.List.TailedLinkedList import TailedLinkedList


class Node:
    def __init__(self, d=None, n=None):
        self.d = d
        self.n = n


def test_tailed_linked_list_type():
    assert isinstance(TailedLinkedList(), MutableSequence)
    assert isinstance(TailedLinkedList(), LinkedList)


def test_tailed_linked_list_iterator():
    assert list(TailedLinkedList()) == []
    l = TailedLinkedList([0, 1, 2, 3, 4, 5])
    assert list(l) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]


def test_tailed_linkedin_list_printer():
    assert TailedLinkedList().to_string() == "None (T,H)"
    assert TailedLinkedList([0]).to_string() == "None <─ (T) 0 (H)"
    assert TailedLinkedList([0, 1]).to_string() == "None <─ (T) 0 <─ 1 (H)"
    assert TailedLinkedList([0, 1, 2]).to_string() == "None <─ (T) 0 <─ 1 <─ 2 (H)"
    assert TailedLinkedList().to_string(reverse=True) == "(H,T) None"
    assert TailedLinkedList([0]).to_string(reverse=True) == "(H) 0 (T) ─> None"
    assert TailedLinkedList([0, 1]).to_string(reverse=True) == "(H) 1 ─> 0 (T) ─> None"
    assert TailedLinkedList([0, 1, 2]).to_string(reverse=True) == "(H) 2 ─> 1 ─> 0 (T) ─> None"
    assert TailedLinkedList().to_string(include_end=False) == "(T,H)"
    assert TailedLinkedList([0]).to_string(include_end=False) == "(T) 0 (H)"
    assert TailedLinkedList([0, 1]).to_string(include_end=False) == "(T) 0 <─ 1 (H)"
    assert TailedLinkedList([0, 1, 2]).to_string(include_end=False) == "(T) 0 <─ 1 <─ 2 (H)"
    assert TailedLinkedList().to_string(mark_head=False, mark_tail=False) == "None"
    assert TailedLinkedList([0]).to_string(mark_head=False, mark_tail=False) == "None <─ 0"
    assert TailedLinkedList([0, 1]).to_string(mark_head=False, mark_tail=False) == "None <─ 0 <─ 1"
    assert TailedLinkedList([0, 1, 2]).to_string(mark_head=False, mark_tail=False) == "None <─ 0 <─ 1 <─ 2"
    assert TailedLinkedList().to_string(include_end=False, mark_head=False, mark_tail=False) == "None"
    assert TailedLinkedList([0]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0"
    assert TailedLinkedList([0, 1]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0 <─ 1"
    assert TailedLinkedList([0, 1, 2]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0 <─ 1 <─ 2"


def test_tailed_linked_list_equal():
    nodes = [Node(0), Node(1), Node(2)]
    assert TailedLinkedList().equal(TailedLinkedList(head=None, data_name="d", next_name="n"))
    assert TailedLinkedList([0]).equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))
    nodes[0].n = nodes[1]
    assert TailedLinkedList([1, 0]).equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))
    nodes[1].n = nodes[2]
    assert TailedLinkedList([2, 1, 0]).equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))


def test_tailed_linked_list_copy():
    nodes = [Node(0), Node(1), Node(2)]
    assert TailedLinkedList().copy().equal(TailedLinkedList(head=None, data_name="d", next_name="n"))
    assert TailedLinkedList([0]).copy().equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))
    nodes[0].n = nodes[1]
    assert TailedLinkedList([1, 0]).copy().equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))
    nodes[1].n = nodes[2]
    assert TailedLinkedList([2, 1, 0]).copy().equal(TailedLinkedList(head=nodes[0], data_name="d", next_name="n"))


def test_tailed_linked_list_clear():
    l = TailedLinkedList([2, 1, 0])
    l.clear()
    assert l.equal(TailedLinkedList())


def test_tailed_linked_list_reverse():
    l = TailedLinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    l.reverse()
    assert list(l) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert l.get_data(l.head) == 0
    assert l.get_data(l.tail) == 9
    l.reverse(group_size=5)
    assert list(l) == [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 5
    l.reverse(end=7, group_size=3, remainder_on_left=False)
    assert list(l) == [7, 6, 5, 0, 9, 8, 2, 1, 3, 4]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 7
    l.reverse(end=4, group_size=2, remainder_on_left=True)
    assert list(l) == [7, 5, 6, 9, 0, 8, 2, 1, 3, 4]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 7
    l.reverse(start=5, group_size=2, remainder_on_left=True)
    assert list(l) == [7, 5, 6, 9, 0, 8, 1, 2, 4, 3]
    assert l.get_data(l.head) == 3
    assert l.get_data(l.tail) == 7




