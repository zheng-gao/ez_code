from ezcode.string import rotate_char


def test_rotate_char():
    rotate_factor = 3
    data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    benchmark = "defghijklmnopqrstuvwxyzabcDEFGHIJKLMNOPQRSTUVWXYZABC3456789012!@#$%^&*()"
    for c1, c2 in zip(data, benchmark):
        assert rotate_char(c1, rotate_factor) == c2
