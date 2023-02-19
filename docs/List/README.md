# List
1. [Linked List](1_LinkedList.md)<br>
2. [Tailed Linked List](2_TailedLinkedList.md)<br>
3. [Doubly Linked List](3_DoublyLinkedList.md)<br>
---
## Inheritance Hierarchy
```
collections.abc.MutableSequence
                       │
                       ▼
                   LinkedList    ───► Stack
                       │     
                       ▼
                TailedLinkedList ───► Stack, Queue
                       │
                       ▼
                DoublyLinkedList ───► Stack, Queue, Deque
```
---
## [Linked List](1_Linked_List.md)
```
                                                  Head
                 ┌──────┐          ┌──────┐     ┌──────┐
                 │ Data │          │ Data │     │ Data │
    ┌──────┐     ├──────┤          ├──────┤     ├──────┤
    │ None │◄────┤ Next │ ... ◄────┤ Next │◄────┤ Next │
    └──────┘     └──────┘          └──────┘     └──────┘
```
## [Tailed Linked List](2_Tailed_Linked_List.md)
```
                   Tail                           Head
                 ┌──────┐          ┌──────┐     ┌──────┐
                 │ Data │          │ Data │     │ Data │
    ┌──────┐     ├──────┤          ├──────┤     ├──────┤
    │ None │◄────┤ Next │ ... ◄────┤ Next │◄────┤ Next │
    └──────┘     └──────┘          └──────┘     └──────┘
```
## [Doubly Linked List](3_Doubly_Linked_List.md)
```
                   Tail                           Head
                 ┌──────┐          ┌──────┐     ┌──────┐
                 │ Data │          │ Data │     │ Data │
    ┌──────┐     ├──────┤          ├──────┤     ├──────┤
    │ None │◄────┤ Next │ ... ◄────┤ Next │◄────┤ Next │
    └──────┘     ├──────┤          ├──────┤     ├──────┤     ┌──────┐
                 │ Prev ├────► ... │ Prev ├────►│ Prev ├────►│ None │
                 └──────┘          └──────┘     └──────┘     └──────┘
```






