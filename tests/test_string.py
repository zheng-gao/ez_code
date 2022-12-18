from ezcode.string import rotate_char, substrings


def test_rotate_char():
    rotate_factor = 3
    data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    benchmark = "defghijklmnopqrstuvwxyzabcDEFGHIJKLMNOPQRSTUVWXYZABC3456789012!@#$%^&*()"
    for c1, c2 in zip(data, benchmark):
        assert rotate_char(c1, rotate_factor) == c2
    for c1, c2 in zip(data, benchmark):
        assert rotate_char(c2, -rotate_factor) == c1


def test_substrings():
    assert substrings("abbbc", unique=True, by_size=False) == [
        'a', 'b', 'c', 'ab', 'bb', 'bc', 'abb', 'bbb', 'bbc', 'abbb', 'bbbc', 'abbbc'
    ]
    assert substrings("abbbc", unique=False, by_size=False) == [
        'a', 'b', 'b', 'b', 'c', 'ab', 'bb', 'bb', 'bc', 'abb', 'bbb', 'bbc', 'abbb', 'bbbc', 'abbbc'
    ]
    assert substrings("abbbc", unique=True, by_size=True) == {
        1: ['a', 'b', 'c'],
        2: ['ab', 'bb', 'bc'],
        3: ['abb', 'bbb', 'bbc'],
        4: ['abbb', 'bbbc'],
        5: ['abbbc']
    }
    assert substrings("abbbc", unique=False, by_size=True) == {
        1: ['a', 'b', 'b', 'b', 'c'],
        2: ['ab', 'bb', 'bb', 'bc'],
        3: ['abb', 'bbb', 'bbc'],
        4: ['abbb', 'bbbc'],
        5: ['abbbc']
    }
