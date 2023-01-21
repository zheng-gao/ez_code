from copy import deepcopy
from collections import deque

from ezcode.Heap.PriorityMap import PriorityMap
from ezcode.Utils.Color import colored_square_string


class GridPathFinder:
    def __init__(self, grid: list[list], row_min: int = None, row_max: int = None, col_min: int = None, col_max: int = None):
        self.grid = grid
        self.row_min = 0 if row_min is None else row_min
        self.row_max = len(grid) - 1 if row_max is None else row_max
        self.col_min = 0 if col_min is None else col_min
        self.col_max = len(grid[0]) - 1 if col_max is None else col_max
        self.offsets = set([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Up, Down, Left, Right

    def __contains__(self, node: tuple[int, int]):
        return self.row_min <= node[0] and node[0] <= self.row_max and self.col_min <= node[1] and node[1] <= self.col_max

    def distance(self, n1, n2, method="manhattan"):
        if method == "manhattan":
            return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

    def value(self, node: tuple[int, int]):
        return self.grid[node[0]][node[1]]

    def neighbors(self, node: tuple[int, int], valid_values: set = None) -> list[tuple[int, int]]:
        valid_neighbors = list()
        for offset in self.offsets:
            neighbor = (node[0] + offset[0], node[1] + offset[1])
            if neighbor in self and (valid_values is None or self.value(neighbor) in valid_values):
                valid_neighbors.append(neighbor)
        return valid_neighbors

    """
    Path finding algorithms Summary:
                        Shortest                Paths    Time           Space    Topology   f_value
    dfs                 no                      1        O(E)           O(N)     1:1        N/A
    backtracking        yes                     All      O(V!)          O(N)     1:1        N/A
    bfs                 yes (fixed step cost)   1        O(E)           O(N)     1:N        N/A
    dijkstra            yes                     1        O(V + ElogV)   O(N)     1:N        h_value = 0 or g_value >> h_value
    A*                  yes                     1        O(V + ElogV)   O(N)     1:N        g_value + h_value

    Notes:
    bfs shortest path only work on fixed step cost
    on fixed step cost (similar to unweighted graph)
        1. dijkstra == bfs
        2. bfs, dijkstra and A* can return early

    A* f_value = g_value + h_value
    The more accurate we can estimate the path length from a node to destination (h_value), the faster A* can run.
    If h_value = 0, which means we don't give any estimation, it becomes Dijkstra, the lower h_value the more nodes to expand
    If h_value is the same as real value, A* won't expand any node and only follow the shortest path
    If h_value is larger than real value, A* won't guarantee the shortest path but it can run faster
    If h_value >> g_value, which means we trust the heuristic path length
    """
    def backtracking(self, source: tuple[int, int], destination: tuple[int, int], valid_values: set = None) -> list[list[tuple[int, int]]]:
        if source not in self or destination not in self or self.value(source) not in valid_values or self.value(destination) not in valid_values:
            return list()
        shortest_paths, path, visited = list(), list([source]), set([source])

        def _backtracking(node: tuple[int, int]):
            if node == destination:
                if shortest_paths and len(path) < len(shortest_paths[0]):
                    shortest_paths.clear()
                shortest_paths.append(path.copy())
                return
            for neighbor in self.neighbors(node, valid_values):
                if neighbor not in visited and (not shortest_paths or len(path) < len(shortest_paths[0])):
                    visited.add(neighbor)
                    path.append(neighbor)
                    _backtracking(neighbor)
                    visited.remove(neighbor)
                    path.pop()

        _backtracking(source)
        return shortest_paths

    def path_dict_to_path(self, path_dict: dict, destination: tuple[int, int]) -> list[tuple[int, int]]:
        if destination not in path_dict:
            return None
        path, parent = deque([destination]), path_dict[destination]
        while parent:
            path.appendleft(parent)
            parent = path_dict[parent] if parent in path_dict else None
        return list(path)

    def dfs(self, source: tuple[int, int], destination: tuple[int, int], valid_values: set = None) -> list[tuple[int, int]]:
        """
            candidates is a Stack
            searched nodes will not be revisited
            does not guarantee the shortest path
        """
        if source not in self or destination not in self or self.value(source) not in valid_values or self.value(destination) not in valid_values:
            return None
        if source == destination:
            return list([source])
        path_dict, visited = dict(), set([source])  # path_dict = {child: parent}
        candidates = list([source])  # stack
        while len(candidates) > 0:
            closest_node = candidates.pop()
            for neighbor in self.neighbors(closest_node, valid_values):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path_dict[neighbor] = closest_node
                    if neighbor == destination:
                        return self.path_dict_to_path(path_dict, destination)
                    candidates.append(neighbor)
        return None

    def bfs(self, source: tuple[int, int], destination: tuple[int, int], valid_values: set = None) -> list[tuple[int, int]]:
        """
            candidates is a Queue
            searched nodes will not be revisited
            guarantee the shortest path
        """
        if source not in self or destination not in self or self.value(source) not in valid_values or self.value(destination) not in valid_values:
            return None
        if source == destination:
            return list([source])
        path_dict, visited = dict(), set([source])  # path_dict = {child: parent}
        candidates = deque([source])  # queue
        while len(candidates) > 0:
            closest_node = candidates.popleft()
            for neighbor in self.neighbors(closest_node, valid_values):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path_dict[neighbor] = closest_node
                    if neighbor == destination:
                        return self.path_dict_to_path(path_dict, destination)
                    candidates.append(neighbor)
        return None

    def dijkstra(self, source: tuple[int, int], destination: tuple[int, int], valid_values: set = None) -> list[tuple[int, int]]:
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
        """
        if source not in self or destination not in self or self.value(source) not in valid_values or self.value(destination) not in valid_values:
            return None
        if source == destination:
            return list([source])
        path_dict, visited = dict(), set()                  # path_dict = {child: parent}
        candidates = PriorityMap(min_heap=True)
        g_values = {source: 0}                              # g_value: path cost to source
        candidates.push(item=source, priority=0)            # priority = g_value
        while len(candidates) > 0:
            closest_node = candidates.pop()
            visited.add(closest_node)                       # <------------| visit node after poping from candidates
            for neighbor in self.neighbors(closest_node, valid_values):  # |
                if neighbor not in visited:                 # <------------| searched neighbor can be updated again
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    distance = g_values[closest_node] + 1   # Fixed step cost == self.distance(closest_node, neighbor, "manhattan") == 1
                    if distance < g_values[neighbor]:
                        g_values[neighbor] = distance
                        candidates.push(item=neighbor, priority=distance)
                        path_dict[neighbor] = closest_node
                        if neighbor == destination:  # return early
                            return self.path_dict_to_path(path_dict, destination)
        return self.path_dict_to_path(path_dict, destination)

    def a_star(self, source: tuple[int, int], destination: tuple[int, int], valid_values: set = None) -> list[tuple[int, int]]:
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
            h_value = 0, it becomes dijkstra which is slower than A*
            h_value >> g_value, it becomes bfs which does not guarantee the shortest path
        """
        if source not in self or destination not in self or self.value(source) not in valid_values or self.value(destination) not in valid_values:
            return None
        if source == destination:
            return list([source])
        path_dict, visited = dict(), set()  # path_dict = {child: parent}
        candidates = PriorityMap(min_heap=True)
        g_values = {source: 0}                                     # g_value: path cost to source
        h_value = self.distance(source, destination, "manhattan")  # h_value: huristic estimate of the path cost to destination
        f_value = g_values[source] + h_value                       # f_value: g_value + h_value
        candidates.push(item=source, priority=f_value)                           # priority = f_value
        while len(candidates) > 0:
            closest_node = candidates.pop()
            visited.add(closest_node)                       # <------------| visit node after poping from candidates
            for neighbor in self.neighbors(closest_node, valid_values):  # |
                if neighbor not in visited:                 # <------------| searched neighbor can be updated again
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    distance = g_values[closest_node] + 1   # Fixed step cost == self.distance(closest_node, neighbor, "manhattan") == 1
                    if distance < g_values[neighbor]:
                        g_values[neighbor] = distance
                        h_value = self.distance(neighbor, destination, "manhattan")
                        f_value = g_values[neighbor] + h_value
                        candidates.push(item=neighbor, priority=f_value)
                        path_dict[neighbor] = closest_node
                        if neighbor == destination:  # return early
                            return self.path_dict_to_path(path_dict, destination)
        return self.path_dict_to_path(path_dict, destination)

    def print(self, value_color: dict = None, layers: list[dict] = None):
        """
            e.g.
            layers is list of {value, nodes}
            layers = [
                {"value": 5, "nodes": [(1,2), (1,3), (2,3), ...]},
                {"value": 1, "nodes": [(1,3), (1,4), (1,5), ...]},
                ...
            ]
            value_color = {
                0: "White",
                1: "Red",
                2: "Green",
                3: "Yellow",
                ...
            }
        """
        grid = deepcopy(self.grid)
        if layers:
            for layer in layers:
                for node in layer["nodes"]:
                    grid[node[0]][node[1]] = layer["value"]
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if value_color is None:
                    print(grid[row][col], end="")
                else:
                    print(colored_square_string(value_color[grid[row][col]]), end="")
            print()

