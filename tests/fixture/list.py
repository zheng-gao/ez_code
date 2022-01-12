from ezcode.list.singly_linked_list import SinglyLinkedList


class Node:
    def __init__(self, v=None, n=None):
        self.v = v
        self.n = n

    def __repr__(self):
        return f"Node({self.v})"


s_head = Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7, Node(8, Node(9))))))))))
c_head = Node(0, Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7, Node(8, Node(9))))))))))
r_head = Node(9, Node(8, Node(7, Node(6, Node(5, Node(4, Node(3, Node(2, Node(1, Node(0))))))))))
s_list = SinglyLinkedList(head=s_head, data_name="v", next_name="n")
c_list = SinglyLinkedList(head=c_head, data_name="v", next_name="n")
r_list = SinglyLinkedList(head=r_head, data_name="v", next_name="n")
