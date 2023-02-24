from collections.abc import MutableSequence
from ezcode.List.LinkedList import LinkedList
from ezcode.List.TailedLinkedList import TailedLinkedList
from ezcode.List.DoublyLinkedList import DoublyLinkedList


class Node:
    def __init__(self, d=None, n=None, p=None):
        self.d = d
        self.n = n
        self.p = p


def test_doubly_linked_list_type():
    assert isinstance(DoublyLinkedList(), MutableSequence)
    assert isinstance(DoublyLinkedList(), LinkedList)
    assert isinstance(DoublyLinkedList(), TailedLinkedList)
    

def test_doubly_linked_list_iterator():
    assert list(DoublyLinkedList()) == []
    l = DoublyLinkedList([0, 1, 2, 3, 4, 5])
    assert list(l) == [0, 1, 2, 3, 4, 5]
    assert list(reversed(l)) == [5, 4, 3, 2, 1, 0]


def test_doubly_linkedin_list_printer():
    assert DoublyLinkedList().to_string() == "None (T,H) None"
    assert DoublyLinkedList([0]).to_string() == "None <─ (T) 0 (H) ─> None"
    assert DoublyLinkedList([0, 1]).to_string() == "None <─ (T) 0 <─> 1 (H) ─> None"
    assert DoublyLinkedList([0, 1, 2]).to_string() == "None <─ (T) 0 <─> 1 <─> 2 (H) ─> None"
    assert DoublyLinkedList().to_string(reverse=True) == "None (H,T) None"
    assert DoublyLinkedList([0]).to_string(reverse=True) == "None <─ (H) 0 (T) ─> None"
    assert DoublyLinkedList([0, 1]).to_string(reverse=True) == "None <─ (H) 1 <─> 0 (T) ─> None"
    assert DoublyLinkedList([0, 1, 2]).to_string(reverse=True) == "None <─ (H) 2 <─> 1 <─> 0 (T) ─> None"
    assert DoublyLinkedList().to_string(include_end=False) == "(T,H)"
    assert DoublyLinkedList([0]).to_string(include_end=False) == "(T) 0 (H)"
    assert DoublyLinkedList([0, 1]).to_string(include_end=False) == "(T) 0 <─> 1 (H)"
    assert DoublyLinkedList([0, 1, 2]).to_string(include_end=False) == "(T) 0 <─> 1 <─> 2 (H)"
    assert DoublyLinkedList().to_string(mark_head=False, mark_tail=False) == "None"
    assert DoublyLinkedList([0]).to_string(mark_head=False, mark_tail=False) == "None <─ 0 ─> None"
    assert DoublyLinkedList([0, 1]).to_string(mark_head=False, mark_tail=False) == "None <─ 0 <─> 1 ─> None"
    assert DoublyLinkedList([0, 1, 2]).to_string(mark_head=False, mark_tail=False) == "None <─ 0 <─> 1 <─> 2 ─> None"
    assert DoublyLinkedList().to_string(include_end=False, mark_head=False, mark_tail=False) == "None"
    assert DoublyLinkedList([0]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0"
    assert DoublyLinkedList([0, 1]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0 <─> 1"
    assert DoublyLinkedList([0, 1, 2]).to_string(include_end=False, mark_head=False, mark_tail=False) == "0 <─> 1 <─> 2"


def test_doubly_linked_list_equal():
    nodes = [Node(0), Node(1), Node(2)]
    assert DoublyLinkedList().equal(DoublyLinkedList(head=None, data_name="d", next_name="n", prev_name="p"))
    assert DoublyLinkedList([0]).equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))
    nodes[0].n, nodes[1].p = nodes[1], nodes[0]
    assert DoublyLinkedList([1, 0]).equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))
    nodes[1].n, nodes[2].p = nodes[2], nodes[1]
    assert DoublyLinkedList([2, 1, 0]).equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))


def test_doubly_linked_list_copy():
    nodes = [Node(0), Node(1), Node(2)]
    assert DoublyLinkedList().copy().equal(DoublyLinkedList(head=None, data_name="d", next_name="n", prev_name="p"))
    assert DoublyLinkedList([0]).copy().equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))
    nodes[0].n, nodes[1].p = nodes[1], nodes[0]
    assert DoublyLinkedList([1, 0]).copy().equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))
    nodes[1].n, nodes[2].p = nodes[2], nodes[1]
    assert DoublyLinkedList([2, 1, 0]).copy().equal(DoublyLinkedList(head=nodes[0], data_name="d", next_name="n", prev_name="p"))


def test_doubly_linked_list_clear():
    l = DoublyLinkedList([2, 1, 0])
    l.clear()
    assert l.equal(DoublyLinkedList())


def test_doubly_linked_list_reverse():
    l = DoublyLinkedList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    l.reverse()
    assert list(l) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert list(reversed(l)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert l.get_data(l.head) == 0
    assert l.get_data(l.tail) == 9
    l.reverse(group_size=5)
    assert list(l) == [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
    assert list(reversed(l)) == [4, 3, 2, 1, 0, 9, 8, 7, 6, 5]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 5
    l.reverse(end=7, group_size=3, remainder_on_left=False)
    assert list(l) == [7, 6, 5, 0, 9, 8, 2, 1, 3, 4]
    assert list(reversed(l)) == [4, 3, 1, 2, 8, 9, 0, 5, 6, 7]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 7
    l.reverse(end=4, group_size=2, remainder_on_left=True)
    assert list(l) == [7, 5, 6, 9, 0, 8, 2, 1, 3, 4]
    assert list(reversed(l)) == [4, 3, 1, 2, 8, 0, 9, 6, 5, 7]
    assert l.get_data(l.head) == 4
    assert l.get_data(l.tail) == 7
    l.reverse(start=5, group_size=2, remainder_on_left=True)
    assert list(l) == [7, 5, 6, 9, 0, 8, 1, 2, 4, 3]
    assert list(reversed(l)) == [3, 4, 2, 1, 8, 0, 9, 6, 5, 7]
    assert l.get_data(l.head) == 3
    assert l.get_data(l.tail) == 7






