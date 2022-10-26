from ezcode.interval import Interval
from ezcode.interval.algorithm import merge_intervals, overlapping_interval_pairs, min_groups_of_non_overlapping_intervals


def test_interval_overlap():
    # single point
    assert Interval(1, 1).overlap(Interval(1, 1))
    assert not Interval(1, 1, True, True).overlap(Interval(0, 2, True, True))
    assert not Interval(1, 1, right_open=True).overlap(Interval(1, 1))
    assert not Interval(1, 1, right_open=True).overlap(Interval(0, 2))
    assert Interval(1, 5).overlap(Interval(3, 8))
    assert Interval(1, 5).overlap(Interval(3, 4))
    assert not Interval(1, 5).overlap(Interval(6, 8))
    assert Interval(1, 5).overlap(Interval(5, 8))
    assert Interval(1, 5).overlap(Interval(1, 5))
    assert not Interval(1, 5, True, True).overlap(Interval(5, 8, True, True))
    assert Interval(1, 5, True, True).overlap(Interval(1, 5, True, True))
    assert not Interval(1, 5, True).overlap(Interval(5, 8, True))
    assert Interval(1, 5, True).overlap(Interval(1, 5, True))


def test_interval_merge():
    assert Interval(1, 5, data=1).merge(Interval(3, 8, data=2), merge_data=lambda x,y: x+y) == Interval(1, 8, data=3)
    assert Interval(1, 5, data=3).merge(Interval(3, 4, data=4), merge_data=max) == Interval(1, 5, data=4)
    assert Interval(1, 5).merge(Interval(6, 8)) is None
    assert Interval(1, 5, data="i1").merge(Interval(5, 8, data="i2"), merge_data=lambda x,y: x+y) == Interval(1, 8, data="i1i2")
    assert Interval(1, 5, data=1).merge(Interval(1, 5, data=2), merge_data=lambda x,y: x+y) == Interval(1, 5, data=3)
    assert Interval(1, 5, True, True).merge(Interval(5, 8, True, True)) is None
    assert Interval(1, 5, True).merge(Interval(1, 5, True, True)) == Interval(1, 5, True)
    assert Interval(1, 5, True).merge(Interval(5, 8, True)) is None
    assert Interval(1, 5, True).merge(Interval(1, 5)) == Interval(1, 5)


def test_interval_intersect():
    assert Interval(1, 5, data=1).intersect(Interval(3, 8, data=2), intersect_data=lambda x,y: x+y) == Interval(3, 5, data=3)
    assert Interval(1, 5, data=3).intersect(Interval(3, 4, data=4), intersect_data=max) == Interval(3, 4, data=4)
    assert Interval(1, 5).intersect(Interval(6, 8)) is None
    assert Interval(1, 5, data="i1").intersect(Interval(5, 8, data="i2"), intersect_data=lambda x,y: x+y) == Interval(5, 5, data="i1i2")
    assert Interval(1, 5, data=1).intersect(Interval(1, 5, data=2), intersect_data=lambda x,y: x+y) == Interval(1, 5, data=3)
    assert Interval(1, 5, True, True).intersect(Interval(5, 8, True, True)) is None
    assert Interval(1, 5, True).intersect(Interval(1, 5, True, True)) == Interval(1, 5, True, True)
    assert Interval(1, 5, True).intersect(Interval(5, 8, True)) is None
    assert Interval(1, 5, True).intersect(Interval(1, 5)) == Interval(1, 5, True)


def test_merge_intervals():
    assert merge_intervals([]) == []
    assert merge_intervals([Interval(1, 2)]) == [Interval(1, 2)]
    assert merge_intervals([Interval(1, 2), Interval(2, 3), Interval(3, 4)]) == [Interval(1, 4)]
    assert merge_intervals([Interval(1, 2), Interval(3, 4), Interval(5, 6)]) == [Interval(1, 2), Interval(3, 4), Interval(5, 6)]
    assert merge_intervals([
        Interval(3, 4), Interval(1, 2), Interval(2, 5),
        Interval(7, 9), Interval(8, 9), Interval(6, 8)
    ]) == [Interval(1, 5), Interval(6, 9)]


def test_overlapping_interval_pairs():
    assert overlapping_interval_pairs([]) == []
    assert overlapping_interval_pairs([Interval(1, 2)]) == []
    assert overlapping_interval_pairs([Interval(1, 2), Interval(1, 2)]) == [(Interval(1, 2), Interval(1, 2))]
    assert overlapping_interval_pairs([
        Interval(1, 2, True, True), Interval(1, 2, True, True)]) == [(Interval(1, 2, True, True), Interval(1, 2, True, True))]
    assert overlapping_interval_pairs([
        Interval(1, 2), Interval(2, 3), Interval(3, 4)
    ]) == [(Interval(1, 2), Interval(2, 3)), (Interval(2, 3), Interval(3, 4))]
    assert overlapping_interval_pairs([Interval(1, 2), Interval(3, 4), Interval(5, 6)]) == []
    assert overlapping_interval_pairs([
        Interval(3, 4), Interval(1, 2), Interval(2, 5), Interval(7, 9), Interval(8, 9), Interval(6, 8)
    ]) == [
        (Interval(1, 2), Interval(2, 5)), (Interval(2, 5), Interval(3, 4)),
        (Interval(6, 8), Interval(7, 9)), (Interval(6, 8), Interval(8, 9)), (Interval(7, 9), Interval(8, 9))
    ]


def test_min_groups_of_non_overlapping_intervals():
    assert min_groups_of_non_overlapping_intervals([]) == []
    assert min_groups_of_non_overlapping_intervals([Interval(1, 2)]) == [[Interval(1, 2)]]
    assert min_groups_of_non_overlapping_intervals([Interval(1, 2), Interval(2, 3)]) == [[Interval(1, 2)], [Interval(2, 3)]]
    assert min_groups_of_non_overlapping_intervals([
        Interval(1, 2, True, True), Interval(2, 3, True, True)]) == [[Interval(1, 2, True, True), Interval(2, 3, True, True)]]
    assert min_groups_of_non_overlapping_intervals([
        Interval(1, 2), Interval(3, 4), Interval(4, 4)]) == [[Interval(1, 2), Interval(3, 4)], [Interval(4, 4)]]
    assert min_groups_of_non_overlapping_intervals([
        Interval(1, 2, True, True), Interval(3, 4, True, True), Interval(4, 4, True, True)
    ]) == [[Interval(1, 2, True, True), Interval(3, 4, True, True), Interval(4, 4, True, True)]]
    assert min_groups_of_non_overlapping_intervals([
        Interval(3, 4), Interval(1, 2), Interval(2, 5), Interval(7, 9), Interval(8, 9), Interval(6, 8)
    ]) == [[Interval(1, 2), Interval(3, 4), Interval(6, 8)], [Interval(2, 5), Interval(7, 9)], [Interval(8, 9)]]
    assert min_groups_of_non_overlapping_intervals([
        Interval(3, 4, True, True), Interval(1, 2, True, True), Interval(2, 5, True, True),
        Interval(7, 9, True, True), Interval(8, 9, True, True), Interval(6, 8, True, True)
    ]) == [
        [Interval(3, 4, True, True), Interval(6, 8, True, True), Interval(8, 9, True, True)],
        [Interval(1, 2, True, True), Interval(2, 5, True, True), Interval(7, 9, True, True)]
    ]



