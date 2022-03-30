import argparse
import os
import random
import sys

from enum import Enum
from collections import deque
from ezcode.heap import PriorityMap


class Square:
    class State(Enum):
        Void = 0
        Obstacle = 1
        Path = 2
        Searched = 3

    colors = [
        "\033[107m",   # White  0 - Void
        "\033[41m",    # Red    1 - Obstacle
        "\033[42m",    # Green  2 - Path
        "\033[43m",    # Yellow 3 - Searched
        "\033[0m",     # Reset  4
    ]

    characters = [
        ". ",  # 0 - Void
        "@ ",  # 1 - Obstacle
        "+ ",  # 2 - Path
        "S ",  # 3 - Searched
    ]

    def __init__(self, state, size: int = 2, text_only=False):
        self.state = state
        self.size = size
        self.text_only = text_only

    def __str__(self):
        if self.text_only:
            return Square.characters[self.state.value]
        return Square.colors[self.state.value] + " " * self.size + Square.colors[-1]


class Maze:
    def __init__(self, row: int = 10, col: int = 10, obstacle_percentage=0.1, text_only=False, show_searched=False):
        self.row_len = row
        self.col_len = col
        self.maze = None
        self.obstacle_percentage = obstacle_percentage
        self.text_only = text_only
        self.show_searched = show_searched

    def build_maze(self, maze=None):
        if maze is None:
            self.maze = [[None for _ in range(self.col_len)] for _ in range(self.row_len)]
            obstacles = self.row_len * self.col_len * self.obstacle_percentage
            for row in range(self.row_len):
                for col in range(self.col_len):
                    rand = random.randrange(self.row_len * self.col_len)
                    self.maze[row][col] = Square.State.Obstacle if rand < obstacles else Square.State.Void
        else:
            self.row_len, self.col_len = len(maze), len(maze[0])
            self.maze = [[None for _ in range(self.col_len)] for _ in range(self.row_len)]
            for row in range(self.row_len):
                for col in range(self.col_len):
                    self.maze[row][col] = Square.State(maze[row][col])

    def copy_maze(self):
        maze_copy = [[None for _ in range(self.col_len)] for _ in range(self.row_len)]
        for row in range(self.row_len):
            for col in range(self.col_len):
                maze_copy[row][col] = self.maze[row][col]
        return maze_copy

    def print_maze(self, maze, clear=False):
        if clear:
            os.system("clear")
        print()
        for row in range(len(maze)):
            print("    ", end="")
            for col in range(len(maze[row])):
                print(Square(state=maze[row][col], text_only=self.text_only), end="")
            print()
        print()

    def validate_selection(self, selection: str):
        if selection == "exit":
            sys.exit()
        numbers = selection.split(",")
        if len(numbers) != 2:
            raise ValueError(f"[Error] Invalid delimiter: \"{selection}\"")
        try:
            row, col = int(numbers[0]), int(numbers[1])
        except ValueError:
            raise ValueError(f"[Error] Invalid selection: \"{selection}\"")
        if row < 0 or row >= self.row_len:
            raise ValueError(f"[Error] Invalid row: \"{row}\"")
        if col < 0 or col >= self.col_len:
            raise ValueError(f"[Error] Invalid column: \"{col}\"")
        if self.maze[row][col] == Square.State.Obstacle:
            raise ValueError(f"[Error] [{row}][{col}] is occupied!")
        return (row, col)

    def prompt_for_selection(self, name):
        while True:
            prompt = f"Select {name} ([0 ~ {self.row_len - 1}],[0 ~ {self.col_len - 1}]): "
            try:
                return self.validate_selection(input(prompt))
            except ValueError as e:
                print(e)

    def approachable_neighbors(self, node) -> list:
        row, col = node
        neighbor_list = list()
        if row > 0 and self.maze[row - 1][col] == Square.State.Void:
            neighbor_list.append((row - 1, col))
        if col > 0 and self.maze[row][col - 1] == Square.State.Void:
            neighbor_list.append((row, col - 1))
        if row + 1 < self.row_len and self.maze[row + 1][col] == Square.State.Void:
            neighbor_list.append((row + 1, col))
        if col + 1 < self.col_len and self.maze[row][col + 1] == Square.State.Void:
            neighbor_list.append((row, col + 1))
        return neighbor_list

    def path_dict_to_path_list(self, path_dict, destination):
        path_list = list([destination])
        parent = path_dict[destination]
        while parent:
            path_list.append(parent)
            parent = path_dict[parent] if parent in path_dict else None
        return path_list[::-1]

    """
    Path finding algorithms Summary:
             Shortest Path    Searched Area     f_value
    bfs         no               larger         h_value >> g_value
    dfs         yes              largest        N/A
    dijkstra    yes              larger         h_value =0
    A*          yes              small          g_value + h_value

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

    def dfs(self, source, destination):
        """
            candidates is a Stack
            searched nodes will not be revisited
            does not guarantee the shortest path
        """
        path_dict, searched, candidates = dict(), set([source]), list()  # path_dict = {child: parent}
        candidates.append(source)
        while len(candidates) > 0:
            node = candidates.pop()
            for neighbor in self.approachable_neighbors(node):
                if neighbor == destination:
                    searched.add(neighbor)
                    path_dict[destination] = node
                    return self.path_dict_to_path_list(path_dict, destination), searched
                elif neighbor not in searched:
                    searched.add(neighbor)
                    candidates.append(neighbor)
                    path_dict[neighbor] = node
        return self.path_dict_to_path_list(path_dict, destination), searched

    def bfs(self, source, destination):
        """
            candidates is a Queue
            searched nodes will not be revisited
        """
        path_dict, searched, candidates = dict(), set([source]), deque()  # path_dict = {child: parent}
        candidates.append(source)
        while len(candidates) > 0:
            node = candidates.popleft()
            for neighbor in self.approachable_neighbors(node):
                if neighbor == destination:
                    searched.add(neighbor)
                    path_dict[destination] = node
                    return self.path_dict_to_path_list(path_dict, destination), searched
                elif neighbor not in searched:
                    searched.add(neighbor)
                    candidates.append(neighbor)
                    path_dict[neighbor] = node
        return self.path_dict_to_path_list(path_dict, destination), searched

    def dijkstra(self, source, destination):
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
        """
        path_dict, visited, searched, candidates = dict(), set(), set([source]), PriorityMap(min_heap=True)  # path_dict = {child: parent}
        g_values = {source: 0}                             # g_value: path cost to source
        candidates.push(0, source)                         # priority = g_value
        while len(candidates) > 0:
            _, node = candidates.pop()
            visited.add(node)
            for neighbor in self.approachable_neighbors(node):
                if neighbor == destination:
                    searched.add(neighbor)
                    path_dict[destination] = node
                    return self.path_dict_to_path_list(path_dict, destination), searched
                elif neighbor not in visited:
                    searched.add(neighbor)
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    g_values[neighbor] = min(g_values[neighbor], g_values[node] + 1)
                    candidates.push(g_values[neighbor], neighbor)
                    path_dict[neighbor] = node
        return self.path_dict_to_path_list(path_dict, destination), searched

    def a_star(self, source, destination):
        """
            candidates is a Priority Map
            searched nodes can be put into candidates again
            h_value = 0, it becomes dijkstra which is slower than A*
            h_value >> g_value, it becomes bfs which does not guarantee the shortest path
        """
        def manhattan_distance(source, destination):
            return abs(source[0] - destination[0]) + abs(source[1] - destination[1])

        path_dict, visited, searched, candidates = dict(), set(), set([source]), PriorityMap(min_heap=True)  # path_dict = {child: parent}
        g_values = {source: 0}                             # g_value: path cost to source
        h_value = manhattan_distance(source, destination)  # h_value: huristic estimate of the path cost to destination
        f_value = g_values[source] + h_value               # f_value: g_value + h_value
        candidates.push(f_value, source)                   # priority = f_value
        while len(candidates) > 0:
            _, node = candidates.pop()
            visited.add(node)
            for neighbor in self.approachable_neighbors(node):
                if neighbor == destination:
                    searched.add(neighbor)
                    path_dict[destination] = node
                    return self.path_dict_to_path_list(path_dict, destination), searched
                elif neighbor not in visited:
                    searched.add(neighbor)
                    if neighbor not in g_values:
                        g_values[neighbor] = float("inf")
                    g_values[neighbor] = min(g_values[neighbor], g_values[node] + 1)
                    f_value = g_values[neighbor] + manhattan_distance(source, destination)
                    candidates.push(f_value, neighbor)
                    path_dict[neighbor] = node
        return self.path_dict_to_path_list(path_dict, destination), searched

    def update_maze(self, maze, path, searched):
        if self.show_searched:
            for node in searched:
                maze[node[0]][node[1]] = Square.State.Searched
        for node in path:
            maze[node[0]][node[1]] = Square.State.Path
        return maze

    def run(self, maze=None):
        # maze = [
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        # ]
        # source, destination = (35,29), (33,29)
        self.build_maze(maze)
        self.print_maze(self.maze)
        source = self.prompt_for_selection("start point")
        destination = self.prompt_for_selection("  end point")
        path, searched = self.dfs(source, destination)
        print(f"BFS - path: {len(path)}, searched area: {len(searched)}")
        self.print_maze(self.update_maze(self.copy_maze(), path, searched))
        path, searched = self.bfs(source, destination)
        print(f"DFS - path: {len(path)}, searched area: {len(searched)}")
        self.print_maze(self.update_maze(self.copy_maze(), path, searched))
        path, searched = self.dijkstra(source, destination)
        print(f"Dijkstra - path: {len(path)}, searched area: {len(searched)}")
        self.print_maze(self.update_maze(self.copy_maze(), path, searched))
        path, searched = self.a_star(source, destination)
        print(f"A* - path: {len(path)}, searched area: {len(searched)}")
        self.print_maze(self.update_maze(self.copy_maze(), path, searched))


parser = argparse.ArgumentParser(description="Maze")
parser.add_argument("-r", "--row", dest="row", type=int, default=10, help="Number of rows")
parser.add_argument("-c", "--column", dest="col", type=int, default=10, help="Number of columns")
parser.add_argument("-t", "--text-only", dest="text_only", action="store_true", default=False, help="Print Map in Text")
parser.add_argument("-s", "--show-searched-area", dest="show_searched", action="store_true", default=False)
parser.add_argument("-o", "--obstacles-percentage", dest="op", type=float, default=0.1)
args = parser.parse_args()
if __name__ == "__main__":
    Maze(row=args.row, col=args.col, obstacle_percentage=args.op, text_only=args.text_only, show_searched=args.show_searched).run()
