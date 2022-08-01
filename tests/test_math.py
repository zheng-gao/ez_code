from ezcode.math.discrete import permutation_size, permutations, all_items_permutations, next_lexicographic_permutation
from ezcode.math.discrete import combination_size, combinations, all_subsets, partitions, enumerations
from ezcode.math.calculator import infix_notation_to_reverse_polish_notation
from ezcode.math.calculator import evaluate_reverse_polish_notation
from ezcode.math.calculator import calculate


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


def test_next_lexicographic_permutation():
    assert [1, 3, 2] == next_lexicographic_permutation([1, 2, 3])
    assert [1, 2, 3] == next_lexicographic_permutation([3, 2, 1])
    assert [1, 5, 1] == next_lexicographic_permutation([1, 1, 5])


def test_permutations():
    assert None == permutations(0, None)
    assert [[]] == permutations(0, [])
    assert [[]] == permutations(0, [1, 2, 1])
    benchmark = [
        [1, 2],
        [1, 1],
        [2, 1],
    ]
    assert benchmark == permutations(2, [1, 2, 1])
    benchmark = [
        [1, 2],
        [1, 3],
        [2, 1],
        [2, 3],
        [3, 1],
        [3, 2],
    ]
    assert benchmark == permutations(2, [1, 2, 3])
    benchmark = [
        [2, 1, 3],
        [2, 1, 2],
        [2, 1, 1],
        [2, 3, 1],
        [2, 3, 2],
        [2, 2, 1],
        [2, 2, 3],
        [1, 2, 3],
        [1, 2, 2],
        [1, 2, 1],
        [1, 3, 2],
        [1, 3, 1],
        [1, 1, 2],
        [1, 1, 3],
        [3, 2, 1],
        [3, 2, 2],
        [3, 1, 2],
        [3, 1, 1],
    ]
    assert benchmark == permutations(3, [2, 1, 3, 2, 1])


def test_complete_permutations():
    assert None == all_items_permutations(None)
    assert [[]] == all_items_permutations([])
    assert [[1]] == all_items_permutations([1])
    benchmark = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 2, 1],
        [3, 1, 2],
    ]
    assert benchmark == all_items_permutations([1, 2, 3])
    benchmark = [
        [1, 1, 2],
        [1, 2, 1],
        [2, 1, 1],
    ]
    assert benchmark == all_items_permutations([1, 1, 2])


def test_combinations():
    assert None == combinations(0, None)
    assert [[]] == combinations(0, [])
    assert [[]] == combinations(0, [1, 2, 3])
    benchmark = [
        [1, 1],
        [1, 2],
    ]
    assert benchmark == combinations(2, [1, 2, 1])
    benchmark = [
        [1, 2],
        [1, 3],
        [2, 3],
    ]
    assert benchmark == combinations(2, [1, 2, 3])
    benchmark = [
        [1, 1, 2],
        [1, 1, 3],
        [1, 2, 2],
        [1, 2, 3],
        [2, 2, 3],
    ]
    assert benchmark == combinations(3, [2, 1, 3, 2, 1])
    benchmark = [
        [1, 1, 2, 2],
        [1, 1, 2, 3],
        [1, 2, 2, 3],
    ]
    assert benchmark == combinations(4, [2, 1, 3, 2, 1])


def test_all_subsets():
    benchmark = [
        [],
        [1],
        [2],
        [1, 1],
        [1, 2],
        [1, 1, 2],
    ]
    assert benchmark == all_subsets([1, 2, 1])
    benchmark = [
        [],
        [1],
        [2],
        [3],
        [1, 1],
        [1, 2],
        [1, 3],
        [2, 2],
        [2, 3],
        [1, 1, 2],
        [1, 1, 3],
        [1, 2, 2],
        [1, 2, 3],
        [2, 2, 3],
        [1, 1, 2, 2],
        [1, 1, 2, 3],
        [1, 2, 2, 3],
        [1, 1, 2, 2, 3],
    ]
    assert benchmark == all_subsets([2, 1, 3, 2, 1])


def test_all_subsets_unique():
    benchmark = [
        [],
        [1],
        [2],
        [3],
        [1, 2],
        [1, 3],
        [2, 3],
        [1, 2, 3],
    ]
    assert benchmark == all_subsets(items=[1, 2, 3], has_duplicate=False)


def test_partition():
    benchmark = [
        [[1, 2, 3, 4]],
        [[1], [2, 3, 4]],
        [[1], [2], [3, 4]],
        [[1], [2], [3], [4]],
        [[1], [2, 3], [4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3], [4]],
        [[1, 2, 3], [4]]
    ]
    assert benchmark == partitions([1, 2, 3, 4])


def test_enumerations():
    item_lists = [
        ['a', 'b'],
        ['X', 'Y'],
        [1, 2, 3],
    ]
    benchmark = [
        ['a', 'X', 1],
        ['a', 'X', 2],
        ['a', 'X', 3],
        ['a', 'Y', 1],
        ['a', 'Y', 2],
        ['a', 'Y', 3],
        ['b', 'X', 1],
        ['b', 'X', 2],
        ['b', 'X', 3],
        ['b', 'Y', 1],
        ['b', 'Y', 2],
        ['b', 'Y', 3]
    ]
    assert benchmark == enumerations(item_lists, recursive=True)
    assert benchmark == enumerations(item_lists, recursive=False)


def test_calculator():
    arithmetic_expression = "-2/-1 + √4!^2*((-1 + 5) -2)*4/ 2^2"
    rpn = infix_notation_to_reverse_polish_notation(arithmetic_expression)
    assert rpn == [-2, -1, '/', 4, '!', '√', 2, '^', -1, 5, '+', 2, '-', '*', 4, '*', 2, 2, '^', '/', '+']
    assert evaluate_reverse_polish_notation(rpn) == 49.99999999999999
    assert calculate(arithmetic_expression) == 49.99999999999999























