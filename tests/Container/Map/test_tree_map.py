from ezcode.Container.Map.TreeMap import TreeMap


def test_tree_map_set_get_item():
    tm = TreeMap()
    tm[5] = "Five"
    tm[9] = "Nine"
    tm[3] = "Three"
    tm[8] = "Eight"
    tm[6] = "Six"
    tm[1] = "One"
    tm[0] = "Zero"
    tm[4] = "Four"
    tm[7] = "Seven"
    tm[2] = "Two"
    assert list(tm.keys()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(tm.keys(reverse=True)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9][::-1]
    assert list(tm.values()) == ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    assert list(tm.values(reverse=True)) == ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'][::-1]
    assert list(tm.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (3, "Three"), (4, "Four"),
        (5, "Five"), (6, "Six"), (7, "Seven"), (8, "Eight"), (9, "Nine")
    ]
    assert list(tm.items(reverse=True)) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (3, "Three"), (4, "Four"),
        (5, "Five"), (6, "Six"), (7, "Seven"), (8, "Eight"), (9, "Nine")
    ][::-1]
    for key, value in zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        ['Zero', 'One', 'Two', 'Three', 'Four','Five', 'Six', 'Seven', 'Eight', 'Nine']
    ):
        assert tm[key] == value


def test_tree_map_delete_item():
    tm = TreeMap([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    del tm[3]
    del tm[7]
    assert list(tm.keys()) == [0, 1, 2, 4, 5, 6, 8, 9]
    assert list(tm.values()) == [
        'Zero', 'One', 'Two', 'Four',
        'Five', 'Six', 'Eight', 'Nine'
    ]
    assert list(tm.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (4, "Four"),
        (5, "Five"), (6, "Six"), (8, "Eight"), (9, "Nine")
    ]
    del tm[3]
    del tm[5]
    del tm[0]
    del tm[9]
    assert list(tm.keys()) == [1, 2, 4, 6, 8]
    assert list(tm.keys(reverse=True)) == [1, 2, 4, 6, 8][::-1]
    assert list(tm.values()) == ['One', 'Two', 'Four', 'Six', 'Eight']
    assert list(tm.values(reverse=True)) == ['One', 'Two', 'Four', 'Six', 'Eight'][::-1]
    assert list(tm.items()) == [(1, "One"), (2, "Two"), (4, "Four"), (6, "Six"), (8, "Eight")]
    assert list(tm.items(reverse=True)) == [(1, "One"), (2, "Two"), (4, "Four"), (6, "Six"), (8, "Eight")][::-1]
    tm.clear()
    assert list(tm.keys()) == []
    assert list(tm.values()) == []
    assert list(tm.items()) == []


def test_tree_map_update_item():
    tm = TreeMap([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    tm[3] = "3"
    tm[7] = "SEVEN"
    tm[2] = "Two"  # no change
    assert tm[3] == "3"
    assert tm[7] == "SEVEN"
    assert tm[2] == "Two"
    assert list(tm.keys()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(tm.values()) == [
        'Zero', 'One', 'Two', '3', 'Four',
        'Five', 'Six', 'SEVEN', 'Eight', 'Nine'
    ]
    assert list(tm.items()) == [
        (0, "Zero"), (1, "One"), (2, "Two"), (3, "3"), (4, "Four"),
        (5, "Five"), (6, "Six"), (7, "SEVEN"), (8, "Eight"), (9, "Nine")
    ]


def test_tree_map_contains():
    tm = TreeMap([
        (5, "Five"), (9, "Nine"), (3, "Three"), (8, "Eight"), (6, "Six"),
        (1, "One"), (0, "Zero"), (4, "Four"), (7, "Seven"), (2, "Two")
    ])
    assert 5 in tm
    assert 8 in tm
    assert 10 not in tm
    del tm[4]
    assert 4 not in tm
    del tm[5]
    assert 5 not in tm



