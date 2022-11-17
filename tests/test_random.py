from ezcode.random import RandomMultiSet


def test_random_multi_set():
    rm_set = RandomMultiSet()
    rm_set.add("a")
    rm_set.add("a")
    rm_set.add("b")
    rm_set.add("a")
    assert rm_set.item_indices == {"a": {0, 1, 3}, "b": {2}}
    assert rm_set.items == ["a", "a", "b", "a"]
    rm_set.remove("b")
    assert rm_set.item_indices == {"a": {0, 1, 2}}
    assert rm_set.items == ["a", "a", "a"]
    rm_set.remove("a")
    assert rm_set.item_indices == {"a": {0, 1}}
    assert rm_set.items == ["a", "a"]
    rm_set.remove("a")
    assert rm_set.item_indices == {"a": {0}}
    assert rm_set.items == ["a"]
    rm_set.remove("a")
    assert rm_set.item_indices == {}
    assert rm_set.items == []
    rm_set.add("a")
    rm_set.add("a")
    rm_set.add("b")
    rm_set.add("b")
    rm_set.add("c")
    rm_set.add("c")
    assert rm_set.item_indices == {"a": {0, 1}, "b": {2, 3}, "c": {4, 5}}
    assert rm_set.items == ["a", "a", "b", "b", "c", "c"]
    rm_set.remove("a")
    rm_set.remove("a")
    assert rm_set.item_indices == {"b": {2, 3}, "c": {0, 1}}
    assert rm_set.items == ["c", "c", "b", "b"]
    rm_set.remove("c")
    rm_set.remove("c")
    assert rm_set.item_indices == {"b": {0, 1}}
    assert rm_set.items == ["b", "b"]
