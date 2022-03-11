from ezcode.backpack import Backpack


def test_backpack():
    assert 35 == Backpack.max_value_2d(capacity=4, weights=[3, 1, 4], values=[20, 15, 30], iterate_weights_first=True)
    assert 35 == Backpack.max_value_2d(capacity=4, weights=[3, 1, 4], values=[20, 15, 30], iterate_weights_first=False)
    assert 35 == Backpack.max_value_1d(capacity=4, weights=[3, 1, 4], values=[20, 15, 30])
    assert 60 == Backpack.max_value_unlimited_items(capacity=4, weights=[3, 1, 4], values=[20, 15, 30], iterate_weights_first=True)
    assert 60 == Backpack.max_value_unlimited_items(capacity=4, weights=[3, 1, 4], values=[20, 15, 30], iterate_weights_first=False)
