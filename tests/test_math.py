from ezcode.array.utils import is_copied
from ezcode.math.permutation import permutation_size, permutations, permutations_with_all_items
from ezcode.math.combination import combination_size


def test_ermutation_size():
    assert permutation_size(0, 0) == 1
    assert permutation_size(3, 0) == 1
    assert permutation_size(3, 1) == 3
    assert permutation_size(3, 3) == 6
    assert permutation_size(4, 2) == 12
    assert permutation_size(5, 3) == 60


def test_combination_size():
    assert combination_size(0, 0) == 1
    assert combination_size(3, 0) == 1
    assert combination_size(3, 1) == 3
    assert combination_size(3, 2) == 3
    assert combination_size(3, 3) == 1
    assert combination_size(4, 2) == 6
    assert combination_size(5, 2) == 10
    assert combination_size(5, 3) == 10


def test_permutations():
    assert is_copied(None, permutations(0, None))
    assert is_copied([[]], permutations(0, []))
    assert is_copied([[]], permutations(0, [1, 2, 3]))
    benchmark = [
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 3],
        [3, 1],
        [3, 2]
    ]
    assert is_copied(benchmark, permutations(2, [1, 2, 3]))
    benchmark = [
        [1, 1, 2],
        [1, 1, 3],
        [1, 2, 1],
        [1, 2, 2],
        [1, 2, 3],
        [1, 3, 1],
        [1, 3, 2],
        [2, 1, 1],
        [2, 1, 2],
        [2, 1, 3],
        [2, 2, 1],
        [2, 2, 3],
        [2, 3, 1],
        [2, 3, 2],
        [3, 1, 1],
        [3, 1, 2],
        [3, 2, 1],
        [3, 2, 2]
    ]
    assert is_copied(benchmark, permutations(3, [1, 1, 2, 2, 3]))


def test_complete_permutations():
    assert is_copied(None, permutations_with_all_items(None))
    assert is_copied([[]], permutations_with_all_items([]))
    assert is_copied([[1]], permutations_with_all_items([1]))
    benchmark = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 2, 1],
        [3, 1, 2]
    ]
    assert is_copied(benchmark, permutations_with_all_items([1, 2, 3]))
    benchmark = [
        [1, 1, 2],
        [1, 2, 1],
        [2, 1, 1]
    ]
    assert is_copied(benchmark, permutations_with_all_items([1, 1, 2]))
