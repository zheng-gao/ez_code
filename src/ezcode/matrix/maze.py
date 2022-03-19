import argparse
import os
import random
import sys

from enum import Enum
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
        self.map = [[None for _ in range(col)] for _ in range(row)]
        self.obstacle_percentage = obstacle_percentage
        self.text_only = text_only
        self.show_searched = show_searched

    def build_map(self):
        obstacles = self.row_len * self.col_len * self.obstacle_percentage
        for row in range(self.row_len):
            for col in range(self.col_len):
                rand = random.randrange(self.row_len * self.col_len)
                self.map[row][col] = Square.State.Obstacle if rand < obstacles else Square.State.Void

    def print_map(self, clear=False):
        if clear:
            os.system("clear")
        print()
        for row in range(self.row_len):
            print("    ", end="")
            for col in range(self.col_len):
                print(Square(state=self.map[row][col], text_only=self.text_only), end="")
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
        if self.map[row][col] == Square.State.Obstacle:
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
        if row > 0 and self.map[row - 1][col] == Square.State.Void:
            neighbor_list.append((row - 1, col))
        if col > 0 and self.map[row][col - 1] == Square.State.Void:
            neighbor_list.append((row, col - 1))
        if row + 1 < self.row_len and self.map[row + 1][col] == Square.State.Void:
            neighbor_list.append((row + 1, col))
        if col + 1 < self.col_len and self.map[row][col + 1] == Square.State.Void:
            neighbor_list.append((row, col + 1))
        return neighbor_list

    # Path finding algorithms
    def dfs(self, row1, col1, row2, col2):
        pass

    def bfs(self, row1, col1, row2, col2):
        pass

    def dijkstra(self, row1, col1, row2, col2):
        pass

    def a_star(self, source, destination):
        def manhattan_distance(source, destination):
            return abs(source[0] - destination[0]) + abs(source[1] - destination[1])

        def a_star_shortest_path(source, destination):
            path, visited, searched, candidates = dict(), set(), set([source]), PriorityMap(min_heap=True)  # path = {child: parent}
            g_values = {source: 0}                               # g_value: path cost to source
            h_value = manhattan_distance(source, destination)    # h_value: huristic estimate of the path cost to destination
            f_value = g_values[source] + h_value                 # f_value: g_value + h_value
            candidates.push(f_value, source)                     # priority = f_value
            while len(candidates) > 0:
                _, node = candidates.pop()
                visited.add(node)
                for neighbor in self.approachable_neighbors(node):
                    if neighbor == destination:
                        searched.add(neighbor)
                        path[destination] = node
                        return path, searched
                    elif neighbor not in visited:
                        searched.add(neighbor)
                        if neighbor not in g_values:
                            g_values[neighbor] = float("inf")
                        g_values[neighbor] = min(g_values[neighbor], g_values[node] + 1)
                        f_value = g_values[neighbor] + manhattan_distance(source, destination)
                        candidates.push(f_value, neighbor)
                        path[neighbor] = node
            return path, searched

        path, searched = a_star_shortest_path(source, destination)
        if self.show_searched:
            for node in searched:
                self.map[node[0]][node[1]] = Square.State.Searched
        parent = path[destination]
        self.map[destination[0]][destination[1]] = Square.State.Path
        while parent:
            self.map[parent[0]][parent[1]] = Square.State.Path
            parent = path[parent] if parent in path else None

    def run(self):
        self.build_map()
        self.print_map()
        source = self.prompt_for_selection("start point")
        destination = self.prompt_for_selection("  end point")
        self.a_star(source, destination)
        self.print_map()


parser = argparse.ArgumentParser(description="Maze")
parser.add_argument("-r", "--row", dest="row", type=int, default=10, help="Number of rows")
parser.add_argument("-c", "--column", dest="col", type=int, default=10, help="Number of columns")
parser.add_argument("-t", "--text-only", dest="text_only", action="store_true", default=False, help="Print Map in Text")
parser.add_argument("-s", "--show-searched-area", dest="show_searched", action="store_true", default=False)
parser.add_argument("-o", "--obstacles-percentage", dest="op", type=float, default=0.1)
args = parser.parse_args()
if __name__ == "__main__":
    Maze(row=args.row, col=args.col, obstacle_percentage=args.op, text_only=args.text_only, show_searched=args.show_searched).run()
