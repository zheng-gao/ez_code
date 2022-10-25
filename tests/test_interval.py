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
    # inclusive boundary on edge
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=True, end_inclusive=True)
    i2 = Interval(data="i2", start=5, end=8, start_inclusive=True, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=True, end_inclusive=True)
    i2 = Interval(data="i2", start=1, end=5, start_inclusive=True, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # exclusive boundary on edge
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=False, end_inclusive=False)
    i2 = Interval(data="i2", start=5, end=8, start_inclusive=False, end_inclusive=False)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=False, end_inclusive=False)
    i2 = Interval(data="i2", start=1, end=5, start_inclusive=False, end_inclusive=False)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # exclusive vs inclusive boundaries
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(data="i2", start=5, end=8, start_inclusive=False, end_inclusive=True)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
    i1 = Interval(data="i1", start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(data="i2", start=1, end=5, start_inclusive=False, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
