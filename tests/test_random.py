from ezcode.random import RandomMultiSet, RandomDictionary


def test_random_multi_set():
    rm_set = RandomMultiSet()
    rm_set.add("a")
    rm_set.add("a")
    rm_set.add("b")
    rm_set.add("a")
    assert rm_set.indices == {"a": {0, 1, 3}, "b": {2}}
    assert rm_set.items == ["a", "a", "b", "a"]
    rm_set.remove("b")
    assert rm_set.indices == {"a": {0, 1, 2}}
    assert rm_set.items == ["a", "a", "a"]
    rm_set.remove("a")
    assert rm_set.indices == {"a": {0, 1}}
    assert rm_set.items == ["a", "a"]
    rm_set.remove("a")
    assert rm_set.indices == {"a": {0}}
    assert rm_set.items == ["a"]
    rm_set.remove("a")
    assert rm_set.indices == {}
    assert rm_set.items == []
    rm_set.add("a")
    rm_set.add("a")
    rm_set.add("b")
    rm_set.add("b")
    rm_set.add("c")
    rm_set.add("c")
    assert rm_set.indices == {"a": {0, 1}, "b": {2, 3}, "c": {4, 5}}
    assert rm_set.items == ["a", "a", "b", "b", "c", "c"]
    rm_set.remove("a")
    rm_set.remove("a")
    assert rm_set.indices == {"b": {2, 3}, "c": {0, 1}}
    assert rm_set.items == ["c", "c", "b", "b"]
    rm_set.remove("c")
    rm_set.remove("c")
    assert rm_set.indices == {"b": {0, 1}}
    assert rm_set.items == ["b", "b"]


def test_random_dictionary():
    r_dict = RandomDictionary()
    r_dict["a"] = "lower"
    r_dict["*"] = "wildcard"
    r_dict["!"] = "punctuation"
    r_dict["b"] = "lower"
    r_dict["B"] = "upper"
    r_dict["?"] = "punctuation"
    assert r_dict.keys == ['a', '*', '!', 'b', 'B', '?']
    assert r_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, 'B': 4, '?': 5}
    assert r_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'B': 'upper', '?': 'punctuation'}
    del r_dict["B"]
    assert r_dict.keys == ['a', '*', '!', 'b', '?']
    assert r_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, '?': 4}
    assert r_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', '?': 'punctuation'}
    del r_dict["?"]
    assert r_dict.keys == ['a', '*', '!', 'b']
    assert r_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1}
    assert r_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard'}
    r_dict["A"] = "upper"
    r_dict["c"] = "lower"
    assert r_dict.keys == ['a', '*', '!', 'b', 'A', 'c']
    assert r_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1, 'A': 4, 'c': 5}
    assert r_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard', 'A': 'upper', 'c': 'lower'}

