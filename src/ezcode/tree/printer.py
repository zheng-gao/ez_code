import math
import random
import sys

from collections import deque
from ezcode.tree.const import *


class BinaryTreePrinter:
    class IndexedNode:
        def __init__(self, index, node):
            self.index = index
            self.node = node

    def __init__(self,
        data_name: str = DATA_NAME, left_name: str = LEFT_NAME, right_name: str = RIGHT_NAME,
        left_wing: str = LEFT_WING, right_wing: str = RIGHT_WING,
        left_wing_head: str = LEFT_WING_HEAD, right_wing_head: str = RIGHT_WING_HEAD,
        left_wing_tail: str = LEFT_WING_TAIL, right_wing_tail: str = RIGHT_WING_TAIL
    ):
        self.data_name = data_name
        self.left_name = left_name
        self.right_name = right_name
        self.left_wing = left_wing
        self.right_wing = right_wing
        self.left_wing_head = left_wing_head 
        self.right_wing_head = right_wing_head
        self.left_wing_tail = left_wing_tail
        self.right_wing_tail = right_wing_tail
        self.tree_depth = 0
        self.max_data_string_length = 0
        self.char_map = None

    def _align_to_center(self, node, is_last_line):
        """ e.g.
        max data string length: 10
        data length: 3
        pre padding length: 4
        post padding length: 3
        pre padding char: -
        post padding char: -
        left wing tail: <
        right wing tail: >
        ---<ABC>--
        """
        pre_padding_length = math.ceil((self.max_data_string_length - len(str(node.__dict__[self.data_name]))) / 2) # even length padding more, use larger mid index
        post_padding_length = self.max_data_string_length - len(str(node.__dict__[self.data_name])) - pre_padding_length
        pre_padding_char = " " * len(self.left_wing) if is_last_line or node.__dict__[self.left_name] is None else self.left_wing
        post_padding_char = " " * len(self.right_wing) if is_last_line or node.__dict__[self.right_name] is None else self.right_wing
        pre_padding_string = f"{pre_padding_char * (pre_padding_length - 1)}{self.left_wing_tail}"
        post_padding_string = f"{self.right_wing_tail}{post_padding_char * (post_padding_length - 1)}"
        
        return f"{pre_padding_string}{str(node.__dict__[self.data_name])}{post_padding_string}"

    def _set_data_string(self, line_to_print, indexed_node, depth):

        def _get_mid_index(depth, index, line_length):
            slot_count = pow(2, depth)
            slot_id = index * 2 - slot_count + 1
            return int(line_length * slot_id / slot_count)

        data_string = self._align_to_center(indexed_node.node, depth == self.tree_depth)
        start_index = _get_mid_index(depth, indexed_node.index, len(line_to_print)) - int(self.max_data_string_length / 2)
        line_to_print[start_index:(start_index + self.max_data_string_length)] = list(data_string)
        if depth != self.tree_depth:
            if indexed_node.node.__dict__[self.left_name] is not None:
                left_child_mid_index = _get_mid_index(depth + 1, indexed_node.index * 2, len(line_to_print))
                line_to_print[(left_child_mid_index + 1):start_index] = list(self.left_wing * (start_index - left_child_mid_index - 1))
                line_to_print[left_child_mid_index] = self.left_wing_head
            if indexed_node.node.__dict__[self.right_name] is not None:
                right_child_mid_index = _get_mid_index(depth + 1, indexed_node.index * 2 + 1, len(line_to_print))
                line_to_print[(start_index + self.max_data_string_length):right_child_mid_index] = list(self.right_wing * (right_child_mid_index - start_index - self.max_data_string_length))
                line_to_print[right_child_mid_index] = self.right_wing_head

    def _collect_tree_info(self, node):
        """ return depth and update max_data_string_length """
        if node is None:
            return 0
        data_str_len = len(str(node.__dict__[self.data_name])) + len(self.left_wing_head) + len(self.right_wing_head) + len(self.left_wing_tail) + len(self.right_wing_tail)
        if data_str_len > self.max_data_string_length:
            self.max_data_string_length = data_str_len
        left_depth = self._collect_tree_info(node.__dict__[self.left_name]) if node.__dict__[self.left_name] is not None else 0
        right_depth = self._collect_tree_info(node.__dict__[self.right_name]) if node.__dict__[self.right_name] is not None else 0
        return max(left_depth, right_depth) + 1

    def _make_char_map(self, node):
        self.char_map = list()
        if node is None:
            return
        self.tree_depth = self._collect_tree_info(node)
        last_line_data_count = pow(2, self.tree_depth - 1)
        last_line_string_length = last_line_data_count * (self.max_data_string_length + 1) - 1 # +one space in between
        """
        [PrePadding][LeftWingTail][Data][RightWingTail][PostPadding][SPACE][PrePadding][LeftWingTail][Data][RightWingTail][PostPadding][SPACE]...
        """
        queue = deque()
        queue.append(BinaryTreePrinter.IndexedNode(1, node))
        depth = 1
        children_found = 0
        children_left = 1
        line_to_print = list(" " * last_line_string_length)  # we have to make it a list because string is immutable
        while len(queue) > 0:
            indexed_node = queue.popleft()
            children_left -= 1
            self._set_data_string(line_to_print, indexed_node, depth)
            if indexed_node.node.__dict__[self.left_name] is not None:
                queue.append(BinaryTreePrinter.IndexedNode(int(indexed_node.index * 2), indexed_node.node.__dict__[self.left_name]))
                children_found += 1
            if indexed_node.node.__dict__[self.right_name] is not None:
                queue.append(BinaryTreePrinter.IndexedNode(int(indexed_node.index * 2) + 1, indexed_node.node.__dict__[self.right_name]))
                children_found += 1
            if children_left == 0:
                self.char_map.append(line_to_print)
                children_left = children_found
                children_found = 0
                line_to_print = list(" " * last_line_string_length)
                depth += 1

    def to_string(self, node, trim_left=True, trim_right=True):
        self._make_char_map(node)
        start_print_index = 0
        end_print_index = len(self.char_map[0])
        if trim_left:  # trim left blank
            for line in self.char_map:
                last_non_blank_index_from_begin = 0
                for char in line:
                    if char == " ":
                        last_non_blank_index_from_begin += 1
                    else:
                        break
                if start_print_index == 0 or last_non_blank_index_from_begin < start_print_index:
                    start_print_index = last_non_blank_index_from_begin
        if trim_right:  # trim right blank
            for line in self.char_map:
                last_non_blank_index_from_end = len(self.char_map[0])
                for char in line[::-1]:
                    if char == " ":
                        last_non_blank_index_from_end -= 1
                    else:
                        break
                if end_print_index == len(self.char_map[0]) or last_non_blank_index_from_end > end_print_index:
                    end_print_index = last_non_blank_index_from_end
        output_string = ""
        for line in self.char_map:
            output_string += "".join(line[start_print_index:end_print_index]) + "\n"
        return output_string

    def print(self, node, trim_left=True, trim_right=True):
        print("\n" + self.to_string(node, trim_left, trim_right))


