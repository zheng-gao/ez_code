from ezcode.interval import Interval


def test_interval_overlaps():
    # overlaps
    i1 = Interval(start=1, end=5)
    i2 = Interval(start=3, end=8)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # contains
    i1 = Interval(start=1, end=5)
    i2 = Interval(start=3, end=4)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # separate
    i1 = Interval(start=1, end=5)
    i2 = Interval(start=6, end=8)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
    # inclusive boundary on edge
    i1 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True)
    i2 = Interval(start=5, end=8, start_inclusive=True, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    i1 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True)
    i2 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # exclusive boundary on edge
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=False)
    i2 = Interval(start=5, end=8, start_inclusive=False, end_inclusive=False)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=False)
    i2 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=False)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)
    # exclusive vs inclusive boundaries
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(start=5, end=8, start_inclusive=False, end_inclusive=True)
    assert not i1.overlaps_with(i2)
    assert not i2.overlaps_with(i1)
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    assert i1.overlaps_with(i2)
    assert i2.overlaps_with(i1)

def test_interval_merge():
    i1 = Interval(start=1, end=5, data=1)
    i2 = Interval(start=3, end=8, data=2)
    assert i1.merge(i2, merge_data=lambda x,y: x+y) == Interval(1, 8, data=3)
    i1 = Interval(start=1, end=5, data=3)
    i2 = Interval(start=3, end=4, data=4)
    assert i1.merge(i2, merge_data=max) == Interval(1, 5, data=4)
    i1 = Interval(start=1, end=5)
    i2 = Interval(start=6, end=8)
    assert i1.merge(i2) == None
    i1 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True, data="i1")
    i2 = Interval(start=5, end=8, start_inclusive=True, end_inclusive=True, data="i2")
    assert i1.merge(i2, merge_data=lambda x,y: x+y) == Interval(1, 8, True, True, "i1i2")
    i1 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True, data=1)
    i2 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True, data=2)
    assert i1.merge(i2, merge_data=lambda x,y: x+y) == Interval(1, 5, True, True, 3)
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=False)
    i2 = Interval(start=5, end=8, start_inclusive=False, end_inclusive=False)
    assert i1.merge(i2) == None
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=False)
    assert i1.merge(i2) == Interval(1, 5, False, True)
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(start=5, end=8, start_inclusive=False, end_inclusive=True)
    assert i1.merge(i2) == None
    i1 = Interval(start=1, end=5, start_inclusive=False, end_inclusive=True)
    i2 = Interval(start=1, end=5, start_inclusive=True, end_inclusive=True)
    assert i1.merge(i2) == Interval(1, 5, True, True)




