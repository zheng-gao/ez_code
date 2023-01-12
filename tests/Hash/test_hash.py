from ezcode.Hash import hash_encode, hash_decode


def test_get_hash():
    assert hash_encode([1, 2, 3, 4]) == 60730
    assert hash_decode(60730, 4) == [1, 2, 3, 4]
