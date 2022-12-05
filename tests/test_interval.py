from ezcode.interval import Interval
from ezcode.interval.algorithm import merge_intervals
from ezcode.interval.algorithm import overlapping_interval_pairs
from ezcode.interval.algorithm import min_groups_of_non_overlapping_intervals
from ezcode.interval.algorithm import skyline
from ezcode.interval.algorithm import most_overlapped_subintervals


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
    assert Interval(1, 5, data=1).merge(Interval(3, 8, data=2), merge_data=lambda x,y: x+y).equal(Interval(1, 8, data=3))
    assert Interval(1, 5, data=3).merge(Interval(3, 4, data=4), merge_data=max).equal(Interval(1, 5, data=4))
    assert Interval(1, 5).merge(Interval(6, 8)) is None
    assert Interval(1, 5, data="i1").merge(Interval(5, 8, data="i2"), merge_data=lambda x,y: x+y).equal(Interval(1, 8, data="i1i2"))
    assert Interval(1, 5, data=1).merge(Interval(1, 5, data=2), merge_data=lambda x,y: x+y).equal(Interval(1, 5, data=3))
    assert Interval(1, 5, True, True).merge(Interval(5, 8, True, True)) is None
    assert Interval(1, 5, True).merge(Interval(1, 5, True, True)).equal(Interval(1, 5, True))
    assert Interval(1, 5, True).merge(Interval(5, 8, True)) is None
    assert Interval(1, 5, True).merge(Interval(1, 5)).equal(Interval(1, 5))


def test_interval_intersect():
    assert Interval(1, 5, data=1).intersect(Interval(3, 8, data=2), intersect_data=lambda x,y: x+y).equal(Interval(3, 5, data=3))
    assert Interval(1, 5, data=3).intersect(Interval(3, 4, data=4), intersect_data=max).equal(Interval(3, 4, data=4))
    assert Interval(1, 5).intersect(Interval(6, 8)) is None
    assert Interval(1, 5, data="i1").intersect(Interval(5, 8, data="i2"), intersect_data=lambda x,y: x+y).equal(Interval(5, 5, data="i1i2"))
    assert Interval(1, 5, data=1).intersect(Interval(1, 5, data=2), intersect_data=lambda x,y: x+y).equal(Interval(1, 5, data=3))
    assert Interval(1, 5, True, True).intersect(Interval(5, 8, True, True)) is None
    assert Interval(1, 5, True).intersect(Interval(1, 5, True, True)).equal(Interval(1, 5, True, True))
    assert Interval(1, 5, True).intersect(Interval(5, 8, True)) is None
    assert Interval(1, 5, True).intersect(Interval(1, 5)).equal(Interval(1, 5, True))


def test_merge_intervals():
    def equal(l1 : list[Interval], l2: list[Interval]):
        if len(l1) != len(l2):
            return False
        for i1, i2 in zip(l1, l2):
            if not i1.equal(i2):
                return False
        return True

    tests = [
        {
            "input": [],
            "benchmark": []
        },
        {
            "input": [Interval(1, 2)],
            "benchmark": [Interval(1, 2)]
        },
        {
            "input": [Interval(1, 2), Interval(2, 3), Interval(3, 4)],
            "benchmark": [Interval(1, 4)]
        },
        {
            "input": [Interval(1, 2), Interval(3, 4), Interval(5, 6)],
            "benchmark": [Interval(1, 2), Interval(3, 4), Interval(5, 6)]
        },
        {
            "input": [Interval(3, 4), Interval(1, 2), Interval(2, 5),Interval(7, 9), Interval(8, 9), Interval(6, 8)],
            "benchmark": [Interval(1, 5), Interval(6, 9)]
        }
    ]
    for i, test in enumerate(tests):
        print(f"test {i}")
        assert equal(merge_intervals(test["input"]), test["benchmark"])


def test_overlapping_interval_pairs():
    def equal(l1: list[tuple[Interval, Interval]], l2: list[tuple[Interval, Interval]]):
        if len(l1) != len(l2):
            return False
        for t1, t2 in zip(l1, l2):
            if not t1[0].equal(t2[0]) or not t1[1].equal(t2[1]):
                return False
        return True

    tests = [
        {
            "input": [],
            "benchmark": []
        },
        {
            "input": [Interval(1, 2)],
            "benchmark": []
        },
        {
            "input": [Interval(1, 2), Interval(1, 2)],
            "benchmark": [(Interval(1, 2), Interval(1, 2))]
        },
        {
            "input": [Interval(1, 2, True, True), Interval(1, 2, True, True)],
            "benchmark": [(Interval(1, 2, True, True), Interval(1, 2, True, True))]
        },
        {
            "input": [Interval(1, 2), Interval(2, 3), Interval(3, 4)],
            "benchmark": [(Interval(1, 2), Interval(2, 3)), (Interval(2, 3), Interval(3, 4))]
        },
        {
            "input": [Interval(1, 2), Interval(3, 4), Interval(5, 6)],
            "benchmark": []
        },
        {
            "input": [Interval(3, 4), Interval(1, 2), Interval(2, 5), Interval(7, 9), Interval(8, 9), Interval(6, 8)],
            "benchmark": [
                (Interval(1, 2), Interval(2, 5)), (Interval(2, 5), Interval(3, 4)), (Interval(6, 8),Interval(7, 9)), 
                (Interval(6, 8), Interval(8, 9)), (Interval(7, 9), Interval(8, 9))
            ]
        }
    ]
    for i, test in enumerate(tests):
        print(f"test {i}")
        assert equal(overlapping_interval_pairs(test["input"]), test["benchmark"])


def test_min_groups_of_non_overlapping_intervals():
    def equal(l1: list[list[Interval]], l2: list[list[Interval]]):
        if len(l1) != len(l2):
            return False
        for sl1, sl2 in zip(l1, l2):
            if len(sl1) != len(sl2):
                return False
            for i1, i2 in zip(sl1, sl2):
                if not i1.equal(i2):
                    return False
        return True

    tests = [
        {
            "input": [],
            "benchmark": []
        },
        {
            "input": [Interval(1, 2)],
            "benchmark": [[Interval(1, 2)]]
        },
        {
            "input": [Interval(1, 2), Interval(2, 3)],
            "benchmark": [[Interval(1, 2)], [Interval(2, 3)]]
        },
        {
            "input": [Interval(1, 2, True, True), Interval(2, 3, True, True)],
            "benchmark": [[Interval(1, 2, True, True), Interval(2, 3, True, True)]]
        },
        {
            "input": [Interval(1, 2), Interval(3, 4), Interval(4, 4)],
            "benchmark": [[Interval(1, 2), Interval(3, 4)], [Interval(4, 4)]]
        },
        {
            "input": [Interval(1, 2, True, True), Interval(3, 4, True, True), Interval(4, 4, True, True)],
            "benchmark": [[Interval(1, 2, True, True), Interval(3, 4, True, True), Interval(4, 4, True, True)]]
        },
        {
            "input": [Interval(3, 4), Interval(1, 2), Interval(2, 5), Interval(7, 9), Interval(8, 9), Interval(6, 8)],
            "benchmark": [[Interval(1, 2), Interval(3, 4), Interval(6, 8)], [Interval(2, 5), Interval(7, 9)], [Interval(8, 9)]]
        },
        {
            "input": [
                Interval(3, 4, True, True), Interval(1, 2, True, True), Interval(2, 5, True, True),
                Interval(7, 9, True, True), Interval(8, 9, True, True), Interval(6, 8, True, True)
            ],
            "benchmark": [
                [Interval(3, 4, True, True), Interval(6, 8, True, True), Interval(8, 9, True, True)],
                [Interval(1, 2, True, True), Interval(2, 5, True, True), Interval(7, 9, True, True)]
            ]
        }
    ]

    for i, test in enumerate(tests):
        print(f"test {i}")
        assert equal(min_groups_of_non_overlapping_intervals(test["input"]), test["benchmark"])


def test_skyline():
    tests = [
        {
            "input": [(1, 3, 5), (1, 5, 3), (1, 6, 1), (2, 4, 4), (3, 6, 2), (4, 7, 1), (2, 5, 1)],
            "benchmark": [(1, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]
        },
        {
            "input": [(2, 9, 10), (3, 7, 15), (5, 12, 12), (15, 20, 10), (19, 24, 8)],
            "benchmark": [(2, 10), (3, 15), (7, 12), (12, 0), (15, 10), (20, 8), (24, 0)]
        },
        {
            "input": [(0, 2, 3), (2, 5, 3)],
            "benchmark": [(0, 3), (5, 0)]
        },
    ]
    for i, test in enumerate(tests):
        print(f"test {i}")
        assert skyline(test["input"]) == test["benchmark"]


def test_most_overlapped_subintervals():
    assert most_overlapped_subintervals([(1, 2), (2, 3)]) == (2, [(2, 2)])
    assert most_overlapped_subintervals([(0, 10), (5, 12), (8, 13), (11, 12)]) == (3, [(8, 10), (11, 12)])
    assert most_overlapped_subintervals([(1, 5), (2, 8), (3, 6), (4, 7)]) == (4, [(4, 5)])
    data = [
        (1920, 1954),
        (1931, 1975),
        (1921, 1922),
        (1992, 2007),
        (1953, 2017),
        (1700, 1722),
        (2016, 2017),
        (1930, 2001),
        (1990, 2011),
        (1967, 2019),
        (1905, 1987),
        (1990, 2018),
        (1998, 2015),
        (1993, 2019)
    ]
    assert most_overlapped_subintervals(data) == (8, [(1998, 2001)])

