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
        if not paths:
            return not path
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
            [1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1, 0]
        ]
    )
    tests = [
        {   # source is out of range
            "benchmark": [],
            "source": (0, 9), "destination": (2, 2), "valid_values": set([1])
        },
        {   # destination is out of range
            "benchmark": [],
            "source": (1, 1), "destination": (9, 2), "valid_values": set([0])
        },
        {   # source & destination are both in valid cells but not connected
            "benchmark": [],
            "source": (0, 0), "destination": (2, 2), "valid_values": set([1])
        },
        {   # source & destination both are invalid
            "benchmark": [],
            "source": (1, 2), "destination": (3, 2), "valid_values": set([1])
        },
        {   # source is invalid, destination is valid
            "benchmark": [],
            "source": (2, 2), "destination": (2, 4), "valid_values": set([0])
        },
        {   # source is valid, destination is invalid
            "benchmark": [],
            "source": (1, 2), "destination": (2, 5), "valid_values": set([0])
        }, 
        {
            "benchmark": [[(2, 4)]],
            "source": (2, 4), "destination": (2, 4), "valid_values": set([0])
        }, 
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
    dfs_benchmarks = {
        7: [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2)],
        8: [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (3, 5), (3, 4)],
        9: [(3, 4), (3, 5), (3, 6), (2, 6), (1, 6), (1, 5), (0, 5)]
    }
    for i, t in enumerate(tests):
        assert in_paths(grid.bfs(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert in_paths(grid.dijkstra(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert in_paths(grid.a_star(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert equal_paths(grid.dfs_backtracking(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        if i in [7, 8, 9]:
            # Found a path but not the shortest one
            assert grid.dfs(t["source"], t["destination"], t["valid_values"]) == dfs_benchmarks[i]
        else:
            assert in_paths(grid.dfs(t["source"], t["destination"], t["valid_values"]), t["benchmark"])







