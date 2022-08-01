from ezcode.grid import init_grid, GridIterator, Grid


def test_init_grid():
    class Data:
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return str(self.data)

    grid = init_grid(2, 3, Data(1))
    grid[0][0].data = 2
    assert grid[0][0].data == 2
    assert grid[0][1].data == 1
    assert grid[1][0].data == 1


def test_grid_iterator():
    size = 4
    grid = init_grid(size, size)
    for row in range(size):
        for col in range(size):
            grid[row][col] = size * row + col
    #  0  1  2  3
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15
    for row in range(size):
        iterator = GridIterator(grid, row, 0, direction="horizontal")
        for col in range(size):
            assert grid[row][col] == next(iterator)
    for col in range(size):
        iterator = GridIterator(grid, 0, col, direction="vertical")
        for row in range(size):
            assert grid[row][col] == next(iterator)
    for i in range(size):
        row_start = size - i - 1
        iterator = GridIterator(grid, row_start, 0, direction="ascending-diagonal")
        for row, col in zip(range(row_start, -1, -1), range(0, i + 1)):
            assert grid[row][col] == next(iterator)
    for i in range(size):
        iterator = GridIterator(grid, 0, i, direction="descending-diagonal")
        for row, col in zip(range(0, size - i), range(i, size - i)):
            print(f"{row}, {col}")
            assert grid[row][col] == next(iterator)


def test_grid_path_finding_algorithm():
    def equal_paths(paths_1, paths_2):
        if len(paths_1) != len(paths_2):
            return False
        indices = set()
        for p1 in paths_1:
            for index, p2 in enumerate(paths_2):
                if p1 == p2:
                    indices.add(index)
        for i in range(len(paths_1)):
            if i not in indices:
                return False
        return True

    def in_paths(path, paths):
        for p in paths:
            if p == path:
                return True
        return False

    grid = Grid(
        [
            [1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0]
        ]
    )
    valid_values = set([0])
    tests = [
        {
            "benchmark": [[(1, 2), (1, 1), (2, 1), (3, 1), (3, 2)]],
            "source": (1, 2), "destination": (3, 2), "valid_values": set([0])
        },
        {
            "benchmark": [[(1, 2), (1, 3), (1, 4), (2, 4), (3, 4)]],
            "source": (1, 2), "destination": (3, 4), "valid_values": set([0])
        },
        {
            "benchmark": [[(3, 4), (2, 4), (1, 4), (1, 5), (0, 5)]],
            "source": (3, 4), "destination": (0, 5), "valid_values": set([0])
        },
        {
            "benchmark": [
                [(3, 4), (2, 4), (1, 4), (1, 5), (0, 5), (0, 6)],
                [(3, 4), (2, 4), (1, 4), (1, 5), (1, 6), (0, 6)],
                [(3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (0, 6)]
            ],
            "source": (3, 4), "destination": (0, 6), "valid_values": set([0])
        },
        {
            "benchmark": [
                [(1, 4), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6)],
                [(1, 4), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6)],
                [(1, 4), (2, 4), (3, 4), (3, 5), (3, 6), (4, 6)],
                [(1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]
            ],
            "source": (1, 4), "destination": (4, 6), "valid_values": set([0])
        }
    ]
    for t in tests:
        assert equal_paths(grid.backtracking(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert in_paths(grid.dijkstra(t["source"], t["destination"], t["valid_values"]), t["benchmark"])





