from collections import Counter
from ezcode.random import RandomMultiSet, RandomKeyValueDictionary, RandomUniqueValueDictionary


def approximately_equals(target, error, value):
    return target * (1 - error) < value and value < target * (1 + error)


def test_random_multi_set():
    rm_set = RandomMultiSet(["a", "a", "b", "a"])
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
    rm_set = RandomMultiSet(["a", "a", "b", "a"])
    counter = Counter()
    iterations, error = 400, 0.2
    for _ in range(iterations):
        counter.update([rm_set.random()])
    assert approximately_equals(target=iterations * (3/4), error=error, value=counter["a"])
    assert approximately_equals(target=iterations * (1/4), error=error, value=counter["b"])


def test_random_key_value_dictionary():
    r_dict = RandomKeyValueDictionary({"a": "lower", "*": "wildcard", "!": "punctuation", "b": "lower", "B": "upper", "?": "punctuation"})
    assert r_dict.key_list == ['a', '*', '!', 'b', 'B', '?']
    assert r_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, 'B': 4, '?': 5}
    assert r_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'B': 'upper', '?': 'punctuation'}
    del r_dict["B"]
    assert r_dict.key_list == ['a', '*', '!', 'b', '?']
    assert r_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, '?': 4}
    assert r_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', '?': 'punctuation'}
    del r_dict["?"]
    assert r_dict.key_list == ['a', '*', '!', 'b']
    assert r_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1}
    assert r_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard'}
    r_dict["A"] = "upper"
    r_dict["c"] = "lower"
    assert r_dict.key_list == ['a', '*', '!', 'b', 'A', 'c']
    assert r_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1, 'A': 4, 'c': 5}
    assert r_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard', 'A': 'upper', 'c': 'lower'}
    key_counter, value_counter, iterations, error = Counter(), Counter(), 600, 0.2
    for _ in range(iterations):
        key_counter.update([r_dict.random_key()])
        value_counter.update([r_dict.random_value()])
    for key in r_dict.keys():
        assert approximately_equals(target=iterations * (1/6), error=error, value=key_counter[key])
    for value in r_dict.values():
        if value == "lower":
            assert approximately_equals(target=iterations * (1/2), error=error, value=value_counter[value])
        else:
            assert approximately_equals(target=iterations * (1/6), error=error, value=value_counter[value])


def test_random_unique_value_dictionary():
    ruq_dict = RandomUniqueValueDictionary({"a": "lower", "*": "wildcard", "!": "punctuation", "b": "lower", "B": "upper", "?": "punctuation"})
    assert ruq_dict.unique_value_list == ['lower', 'wildcard', 'punctuation', 'upper']
    assert ruq_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2, 'upper': 3}
    assert ruq_dict.value_counter == {'lower': 2, 'punctuation': 2, 'upper': 1, 'wildcard': 1}
    assert ruq_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'B': 'upper', '?': 'punctuation'}
    del ruq_dict["B"]
    assert ruq_dict.unique_value_list == ['lower', 'wildcard', 'punctuation']
    assert ruq_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2}
    assert ruq_dict.value_counter == {'lower': 2, 'punctuation': 2, 'wildcard': 1}
    assert ruq_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', '?': 'punctuation'}
    del ruq_dict["?"]
    assert ruq_dict.unique_value_list == ['lower', 'wildcard', 'punctuation']
    assert ruq_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2}
    assert ruq_dict.value_counter == {'lower': 2, 'punctuation': 1, 'wildcard': 1}
    assert ruq_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower'}
    ruq_dict["A"] = "upper"
    ruq_dict["c"] = "lower"
    assert ruq_dict.unique_value_list == ['lower', 'wildcard', 'punctuation', 'upper']
    assert ruq_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2, 'upper': 3}
    assert ruq_dict.value_counter == {'lower': 3, 'punctuation': 1, 'wildcard': 1, 'upper': 1}
    assert ruq_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'A': 'upper', 'c': 'lower'}
    counter, iterations, error = Counter(), 400, 0.2
    for _ in range(iterations):
        counter.update([ruq_dict.random_value()])
    for value in ruq_dict.unique_value_list:
        assert approximately_equals(target=iterations * (1/4), error=error, value=counter[value])

