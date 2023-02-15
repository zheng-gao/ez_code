# List
1. [Linked List](1_Linked_List.md)<br>
2. [Tailed Linked List](2_Tailed_Linked_List.md)<br>
3. [Doubly Linked List](3_Doubly_Linked_List.md)<br>
---
## Linked List
```
                                                  Head
                 ┌──────┐          ┌──────┐     ┌──────┐
                 │ Data │          │ Data │     │ Data │
    ┌──────┐     ├──────┤          ├──────┤     ├──────┤
    │ None │◄────┤ Next │ ... ◄────┤ Next │◄────┤ Next │
    └──────┘     └──────┘          └──────┘     └──────┘
```
## Tailed Linked List
```
                   Tail                           Head
                 ┌──────┐          ┌──────┐     ┌──────┐
                 │ Data │          │ Data │     │ Data │
    ┌──────┐     ├──────┤          ├──────┤     ├──────┤
    │ None │◄────┤ Next │ ... ◄────┤ Next │◄────┤ Next │
    └──────┘     └──────┘          └──────┘     └──────┘
```
## Doubly Linked List
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






