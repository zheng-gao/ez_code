from ezcode.grid.utils import init_grid
from ezcode.grid.iterator import GridIteratorFactory 
from ezcode.grid.pathfinder import PathFinder


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
    grid = [
        [ 0,  1,  2,  3,  4],
        [ 5,  6,  7,  8,  9],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24]
    ]
    size = len(grid)
    for row in range(size):
        iterator = GridIteratorFactory.get(grid, row, 0, iterator="horizontal")
        for col in range(size):
            assert grid[row][col] == next(iterator)
        iterator = GridIteratorFactory.get(grid, row, size - 1, iterator="horizontal", reverse=True)
        for col in range(size - 1, -1, -1):
            assert grid[row][col] == next(iterator)
    for col in range(size):
        iterator = GridIteratorFactory.get(grid, 0, col, iterator="vertical")
        for row in range(size):
            assert grid[row][col] == next(iterator)
        iterator = GridIteratorFactory.get(grid, size - 1, col, iterator="vertical", reverse=True)
        for row in range(size - 1, -1, -1):
            assert grid[row][col] == next(iterator)
    for i in range(size):
        iterator = GridIteratorFactory.get(grid, 0, i, iterator="major_diagonal")
        for row, col in zip(range(0, size - i), range(i, size - i)):
            assert grid[row][col] == next(iterator)
        iterator = GridIteratorFactory.get(grid, size - 1, i, iterator="major_diagonal", reverse=True)
        for row, col in zip(range(size - 1, size - i - 2, -1), range(i, size - i - 2, -1)):
            assert grid[row][col] == next(iterator)
    for i in range(size):
        iterator = GridIteratorFactory.get(grid, size - i - 1, 0, iterator="minor_diagonal")
        for row, col in zip(range(size - i - 1, -1, -1), range(0, i + 1)):
            assert grid[row][col] == next(iterator)
        iterator = GridIteratorFactory.get(grid, i, size - 1, iterator="minor_diagonal", reverse=True)
        for row, col in zip(range(i, size), range(size - 1, size - i - 2)):
            assert grid[row][col] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 0, 0, iterator="spiral")
    benchmark = [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5, 6, 7, 8, 13, 18, 17, 16, 11, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 0, 0, iterator="spiral", reverse=True)
    benchmark = [0, 5, 10, 15, 20, 21, 22, 23, 24, 19, 14, 9, 4, 3, 2, 1, 6, 11, 16, 17, 18, 13, 8, 7, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 1, 0, iterator="spiral")
    benchmark = [5, 0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 16, 11, 6, 7, 8, 13, 18, 17, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 1, 2, iterator="spiral", reverse=True)
    benchmark = [7, 6, 11, 16, 17, 18, 13, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 4, 3, iterator="spiral")
    benchmark = [23, 22, 21, 20, 15, 10, 5, 0, 1, 2, 3, 4, 9, 14, 19, 18, 17, 16, 11, 6, 7, 8, 13, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 4, 4, iterator="spiral", reverse=True)
    benchmark = [24, 19, 14, 9, 4, 3, 2, 1, 0, 5, 10, 15, 20, 21, 22, 23, 18, 13, 8, 7, 6, 11, 16, 17, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 3, 1, iterator="spiral")
    benchmark = [16, 11, 6, 7, 8, 13, 18, 17, 12]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 1, 3, 3, 2, iterator="spiral", reverse=True)
    benchmark = [8, 7, 6, 11, 16, 17]
    for i in range(len(benchmark)):
        assert benchmark[i] == next(iterator)
    iterator = GridIteratorFactory.get(grid, 2, 2, iterator="spiral")
    for i in iterator:
        assert i == 12


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

    path_finder = PathFinder(
        [
            [1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 1, 0]
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
        assert in_paths(path_finder.bfs(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert in_paths(path_finder.dijkstra(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert in_paths(path_finder.a_star(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        assert equal_paths(path_finder.dfs_backtracking(t["source"], t["destination"], t["valid_values"]), t["benchmark"])
        if i in [7, 8, 9]:
            # Found a path but not the shortest one
            assert path_finder.dfs(t["source"], t["destination"], t["valid_values"]) == dfs_benchmarks[i]
        else:
            assert in_paths(path_finder.dfs(t["source"], t["destination"], t["valid_values"]), t["benchmark"])







