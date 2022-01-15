from ezcode.array.utils import is_copied
from ezcode.math.permutation import selected_permutation_size, selected_permutations, complete_permutations


def test_selected_permutation_size():
    assert selected_permutation_size(0, 0) == 1
    assert selected_permutation_size(3, 0) == 1
    assert selected_permutation_size(3, 1) == 3
    assert selected_permutation_size(3, 3) == 6
    assert selected_permutation_size(4, 2) == 12
    assert selected_permutation_size(5, 3) == 60


def test_selected_permutations():
    assert is_copied(None, selected_permutations(0, None))
    assert is_copied([[]], selected_permutations(0, []))
    assert is_copied([[]], selected_permutations(0, [1,2,3]))
    benchmark = [
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 3],
        [3, 1],
        [3, 2]
    ]
    assert is_copied(benchmark, selected_permutations(2, [1,2,3]))
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
    assert is_copied(benchmark, selected_permutations(3, [1,1,2,2,3]))


def test_complete_permutations():
    assert is_copied(None, complete_permutations(None))
    assert is_copied([[]], complete_permutations([]))
    assert is_copied([[1]], complete_permutations([1]))
    benchmark = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 2, 1],
        [3, 1, 2]
    ]
    assert is_copied(benchmark, complete_permutations([1,2,3]))
    benchmark = [
        [1, 1, 2],
        [1, 2, 1],
        [2, 1, 1]
    ]
    assert is_copied(benchmark, complete_permutations([1,1,3]))

