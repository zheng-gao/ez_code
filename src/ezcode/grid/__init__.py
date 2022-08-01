from collections import deque
from copy import deepcopy

from ezcode.heap import PriorityMap


def init_grid(row: int, col: int, init=None) -> list[list]:
    return [[deepcopy(init) for _ in range(col)] for _ in range(row)]


class GridIterator:
    def __init__(self, grid: list[list], row: int = 0, col: int = 0, direction: str = "horizontal"):
        self.grid = grid
        self.row, self.row_min, self.row_max = row, 0, len(grid) - 1
        self.col, self.col_min, self.col_max = col, 0, len(grid[0]) - 1
        self.direction = direction
        self.valid_directions = {"horizontal", "vertical", "ascending-diagonal", "descending-diagonal"}
        if direction not in self.valid_directions:
            raise ValueError(f"Invalid direction \"{self.direction}\", choose from {self.valid_directions}")

    def __iter__(self):
        return self

    def __next__(self):
        data = None
        try:
            data = self.grid[self.row][self.col]
        except IndexError:
            raise StopIteration
        if self.direction == "horizontal":
            if self.col <= self.col_max:
                self.col += 1
        elif self.direction == "vertical":
            if self.row <= self.row_max:
                self.row += 1
        elif self.direction == "ascending-diagonal":
            if self.row >= self.row_min and self.col <= self.col_max:
                self.row -= 1
                self.col += 1
        elif self.direction == "descending-diagonal":
            if self.row <= self.row_max and self.col <= self.col_max:
                self.row += 1
                self.col += 1
        return data


class Grid:
    def __init__(self, grid: list[list], row_min: int = None, row_max: int = None, col_min: int = None, col_max: int = None):
        self.grid = grid
        self.row_min = 0 if row_min is None else row_min
        self.row_max = len(grid) - 1 if row_max is None else row_max
        self.col_min = 0 if col_min is None else col_min
        self.col_max = len(grid[0]) - 1 if col_max is None else col_max
        self.offsets = set([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Up, Down, Left, Right

    def __contains__(self, node: tuple[int, int]):
        return self.row_min <= node[0] and self.row_max >= node[0] and self.col_min <= node[1] and self.col_max >= node[1]

    def sum(self, n1: tuple[int, int], n2: tuple[int, int]) -> tuple[int, int]:
        return n1[0] + n2[0], n1[1] + n2[1]

    def value(self, node: tuple[int, int]):
        return self.grid[node[0]][node[1]]

    def neighbors(self, node: tuple[int, int], valid_values: set = None, offsets: set = None) -> list[tuple[int, int]]:
        output = list()
        if offsets is None:
            offsets = self.offsets
        for offset in offsets:
            neighbor = self.sum(node, offset)
            if neighbor in self and (valid_values is None or self.value(neighbor) in valid_values):
                output.append(neighbor)
        return output

    """
    Path finding algorithms Summary:
                    Shortest Path     All S-Path     Searched Area    f_value
    bfs             no                no             larger           h_value >> g_value
    dfs             no                no             largest          N/A
    backtracking    yes               yes            largest
    dijkstra        yes               no             larger           h_value =0
    A*              yes               no             small            g_value + h_value

    Notes:
    A* f_value = g_value + h_value
    The more accurate we can estimate the path length from a node to destination (h_value), the faster A* can run.
    If h_value = 0, which means we don't give any estimation, it becomes Dijkstra, the lower h_value the more nodes to expand
    If h_value is the same as real value, A* won't expand any node and only follow the shortest path
    If h_value is larger than real value, A* won't guarantee the shortest path but it can run faster
    If h_value >> g_value, which means we trust the heuristic path length, it becomes bfs and does not guarantee the shortest path
    The heuristic path length must keep the same order as the real ones
    e.g. if a > b then h_a > h_b
    """
    def backtracking(self,
        source: tuple[int, int],
        destination: tuple[int, int],
        valid_values: set = None,
        offsets: set = None
    ) -> list[list[tuple[int, int]]]:
        visited, path, shortest_paths = set([source]), list([source]), list()

        def _backtracking(node: tuple[int, int]):
            if node == destination:
                if shortest_paths and len(path) < len(shortest_paths[0]):
                    shortest_paths.clear()
                shortest_paths.append(path.copy())
                return
            for neighbor in self.neighbors(node, valid_values, offsets):
                if neighbor not in visited and (not shortest_paths or len(path) < len(shortest_paths[0])):
                    visited.add(neighbor)
                    path.append(neighbor)
                    _backtracking(neighbor)
                    visited.remove(neighbor)
                    path.pop()

        _backtracking(source)
        return shortest_paths

    def path_dict_to_path_list(self, path_dict: dict, destination: tuple[int, int]):
        path, parent = deque([destination]), path_dict[destination]
        while parent:
            path.appendleft(parent)
            parent = path_dict[parent] if parent in path_dict else None
        return list(path)

    def dijkstra(self,
        source: tuple[int, int],
        destination: tuple[int, int],
        valid_values: set = None,
        offsets: set = None
    ) -> list[tuple[int, int]]:
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
        """
        if source == destination:
            return list([source])
        path_dict, visited, searched = dict(), set(), set([source])  # path_dict = {child: parent}
        candidates = PriorityMap(min_heap=True)  
        g_values = {source: 0}                                       # g_value: path cost to source
        candidates.push(0, source)                                   # priority = g_value
        while len(candidates) > 0:
            _, closest_node = candidates.pop()
            visited.add(closest_node)
            for neighbor in self.neighbors(closest_node, valid_values, offsets):
                if neighbor not in visited:
                    # searched.add(neighbor)
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    if g_values[closest_node] + 1 < g_values[neighbor]:
                        g_values[neighbor] = g_values[closest_node] + 1
                        candidates.push(g_values[neighbor], neighbor)
                        path_dict[neighbor] = closest_node
        return self.path_dict_to_path_list(path_dict, destination)

    def a_star(self,
        source: tuple[int, int],
        destination: tuple[int, int],
        valid_values: set = None,
        offsets: set = None
    ) -> list[tuple[int, int]]:
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
            h_value = 0, it becomes dijkstra which is slower than A*
            h_value >> g_value, it becomes bfs which does not guarantee the shortest path
        """
        if source == destination:
            return list([source])

        def manhattan_distance(source, destination):
            return abs(source[0] - destination[0]) + abs(source[1] - destination[1])

        path_dict, visited, searched = dict(), set(), set([source])
        candidates = PriorityMap(min_heap=True)            # path_dict = {child: parent}
        g_values = {source: 0}                             # g_value: path cost to source
        h_value = manhattan_distance(source, destination)  # h_value: huristic estimate of the path cost to destination
        f_value = g_values[source] + h_value               # f_value: g_value + h_value
        candidates.push(f_value, source)                   # priority = f_value
        while len(candidates) > 0:
            _, closest_node = candidates.pop()
            visited.add(closest_node)
            for neighbor in self.neighbors(closest_node, valid_values, offsets):
                if neighbor not in visited:
                    # searched.add(neighbor)
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    if g_values[closest_node] + 1 < g_values[neighbor]:
                        g_values[neighbor] = g_values[closest_node] + 1
                        f_value = g_values[neighbor] + manhattan_distance(neighbor, destination)
                        candidates.push(f_value, neighbor)
                        path_dict[neighbor] = closest_node
        return self.path_dict_to_path_list(path_dict, destination)







