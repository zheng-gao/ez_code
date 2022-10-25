from ezcode.interval import Interval


def test_interval_overlaps():
    # overlaps
    i1 = Interval(data="i1", start=1, end=5)
    i2 = Interval(data="i2", start=3, end=8)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # contains
    i1 = Interval(data="i1", start=1, end=5)
    i2 = Interval(data="i2", start=3, end=4)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # separate
    i1 = Interval(data="i1", start=1, end=5)
    i2 = Interval(data="i2", start=6, end=8)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
