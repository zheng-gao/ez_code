from collections import Counter

from ezcode.Math import approximately_equals
from ezcode.Random.RandomDict import RandomKeyValueDict, RandomUniqueValueDict


def test_random_key_value_dict():
    rkv_dict = RandomKeyValueDict({"a": "lower", "*": "wildcard", "!": "punctuation", "b": "lower", "B": "upper", "?": "punctuation"})
    assert len(rkv_dict) == 6
    assert rkv_dict.key_list == ['a', '*', '!', 'b', 'B', '?']
    assert rkv_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, 'B': 4, '?': 5}
    assert rkv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'B': 'upper', '?': 'punctuation'}
    del rkv_dict["B"]
    assert rkv_dict.key_list == ['a', '*', '!', 'b', '?']
    assert rkv_dict.key_index_dict == {'a': 0, '*': 1, '!': 2, 'b': 3, '?': 4}
    assert rkv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', '?': 'punctuation'}
    del rkv_dict["?"]
    assert rkv_dict.key_list == ['a', '*', '!', 'b']
    assert rkv_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1}
    assert rkv_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard'}
    rkv_dict["A"] = "upper"
    rkv_dict["c"] = "lower"
    assert rkv_dict.key_list == ['a', '*', '!', 'b', 'A', 'c']
    assert rkv_dict.key_index_dict == {'a': 0, '!': 2, 'b': 3, '*': 1, 'A': 4, 'c': 5}
    assert rkv_dict.key_value_dict == {'a': 'lower', '!': 'punctuation', 'b': 'lower', '*': 'wildcard', 'A': 'upper', 'c': 'lower'}
    key_counter, value_counter, samples_size, error = Counter(), Counter(), 600, 0.3
    for _ in range(samples_size):
        key_counter.update([rkv_dict.random_key()])
        value_counter.update([rkv_dict.random_value()])
    for key in rkv_dict:
        assert approximately_equals(target=samples_size * (1/6), error=error, value=key_counter[key])
    for value in rkv_dict.values():
        if value == "lower":
            assert approximately_equals(target=samples_size * (1/2), error=error, value=value_counter[value])
        else:
            assert approximately_equals(target=samples_size * (1/6), error=error, value=value_counter[value])


def test_random_unique_value_dict():
    ruv_dict = RandomUniqueValueDict({"a": "lower", "*": "wildcard", "!": "punctuation", "b": "lower", "B": "upper", "?": "punctuation"})
    assert len(ruv_dict) == 6
    assert ruv_dict.unique_value_list == ['lower', 'wildcard', 'punctuation', 'upper']
    assert ruv_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2, 'upper': 3}
    assert ruv_dict.value_counter == {'lower': 2, 'punctuation': 2, 'upper': 1, 'wildcard': 1}
    assert ruv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'B': 'upper', '?': 'punctuation'}
    del ruv_dict["B"]
    assert ruv_dict.unique_value_list == ['lower', 'wildcard', 'punctuation']
    assert ruv_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2}
    assert ruv_dict.value_counter == {'lower': 2, 'punctuation': 2, 'wildcard': 1}
    assert ruv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', '?': 'punctuation'}
    del ruv_dict["?"]
    assert ruv_dict.unique_value_list == ['lower', 'wildcard', 'punctuation']
    assert ruv_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2}
    assert ruv_dict.value_counter == {'lower': 2, 'punctuation': 1, 'wildcard': 1}
    assert ruv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower'}
    ruv_dict["A"] = "upper"
    ruv_dict["c"] = "lower"
    assert ruv_dict.unique_value_list == ['lower', 'wildcard', 'punctuation', 'upper']
    assert ruv_dict.value_index_dict == {'lower': 0, 'wildcard': 1, 'punctuation': 2, 'upper': 3}
    assert ruv_dict.value_counter == {'lower': 3, 'punctuation': 1, 'wildcard': 1, 'upper': 1}
    assert ruv_dict.key_value_dict == {'a': 'lower', '*': 'wildcard', '!': 'punctuation', 'b': 'lower', 'A': 'upper', 'c': 'lower'}
    counter, samples_size, error = Counter(), 400, 0.3
    for _ in range(samples_size):
        counter.update([ruv_dict.random_value()])
    for value in ruv_dict.unique_value_list:
        assert approximately_equals(target=samples_size * (1/4), error=error, value=counter[value])