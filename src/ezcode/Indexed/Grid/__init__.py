from copy import deepcopy


def init_grid(row: int, col: int, init=None) -> list[list]:
    return [[deepcopy(init) for _ in range(col)] for _ in range(row)]
