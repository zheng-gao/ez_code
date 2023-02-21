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

