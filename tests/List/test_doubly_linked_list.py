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



