from ezcode.Dict.TreeDict import TreeDict


def test_tree_dict_set_get_item():
    td = TreeDict()
    td[5] = "Five"
    td[9] = "Nine"
    td[3] = "Three"
    td[8] = "Eight"
    td[6] = "Six"
    td[1] = "One"
    td[0] = "Zero"
    td[4] = "Four"
    td[7] = "Seven"
    td[2] = "Two"
    assert list(td.keys()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(td.values()) == [
        'Zero', 'One', 'Two', 'Three', 'Four',
        'Five', 'Six', 'Seven', 'Eight', 'Nine'
    ]
    assert list(td.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (3, "Three"), (4, "Four"),
        (5, "Five"), (6, "Six"), (7, "Seven"), (8, "Eight"), (9, "Nine")
    ]
    for key, value in zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ['Zero', 'One', 'Two', 'Three', 'Four','Five', 'Six', 'Seven', 'Eight', 'Nine']
    ):
        assert td[key] == value


def test_tree_dict_delete_item():
    td = TreeDict([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    del td[3]
    del td[7]
    assert list(td.keys()) == [0, 1, 2, 4, 5, 6, 8, 9]
    assert list(td.values()) == [
        'Zero', 'One', 'Two', 'Four',
        'Five', 'Six', 'Eight', 'Nine'
    ]
    assert list(td.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (4, "Four"),
        (5, "Five"), (6, "Six"), (8, "Eight"), (9, "Nine")
    ]
    del td[3]
    del td[5]
    del td[0]
    del td[9]
    assert list(td.keys()) == [1, 2, 4, 6, 8]
    assert list(td.values()) == ['One', 'Two', 'Four', 'Six', 'Eight']
    assert list(td.items()) == [(1, "One"), (2, "Two"), (4, "Four"), (6, "Six"), (8, "Eight")]
    td.clear()
    assert list(td.keys()) == []
    assert list(td.values()) == []
    assert list(td.items()) == []


def test_tree_dict_update_item():
    td = TreeDict([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    td[3] = "3"
    td[7] = "SEVEN"
    td[2] = "Two"  # no change
    assert td[3] == "3"
    assert td[7] == "SEVEN"
    assert td[2] == "Two"
    assert list(td.keys()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(td.values()) == [
        'Zero', 'One', 'Two', '3', 'Four',
        'Five', 'Six', 'SEVEN', 'Eight', 'Nine'
    ]
    assert list(td.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (3, "3"), (4, "Four"),
        (5, "Five"), (6, "Six"), (7, "SEVEN"), (8, "Eight"), (9, "Nine")
    ]


def test_tree_dict_contains():
    td = TreeDict([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    assert 5 in td
    assert 8 in td
    assert 10 not in td
    del td[4]
    assert 4 not in td
    del td[5]
    assert 5 not in td



