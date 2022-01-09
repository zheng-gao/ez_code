import pytest

from ezcode.trees.printer import BinaryTreePrinter
from fixtures.trees import s_tree


def test_printer():
    benchmark = """
       ┌──────────(0)──────────┐       
 ┌────(1)────┐           ┌────(2)────┐ 
(3)─┐       (4)       ┌─(5)─┐       (6)
   (7)               (8)   (9)         
"""
    printer = BinaryTreePrinter(data_name="v", left_name="l", right_name="r")
    assert benchmark == "\n" + printer.to_string(s_tree.root)
