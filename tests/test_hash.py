from ezcode.hash import get_hash


def test_get_hash():
    assert get_hash(1, 2, 3) == 3130
    assert get_hash([1, 2, 3]) == 3130
    assert get_hash((1, 2, 3)) == 3130
