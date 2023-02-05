from typing import Iterable

from ezcode.List.LinkedListConstant import DATA_NAME, NEXT_NAME, PREV_NAME
from ezcode.List.TailedLinkedList import TailedLinkedList


class TailedDoublyLinkedList(TailedLinkedList):
    def __init__(self,
        init_data: Iterable = None, head=None, head_copy=None,
        data_name: str = DATA_NAME, next_name: str = NEXT_NAME, prev_name: str = PREV_NAME
    ):
        super().__init__(
            init_data=init_data, head=head, head_copy=head_copy,
            data_name=data_name, next_name=next_name
        )



