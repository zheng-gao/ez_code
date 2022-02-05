

def init_matrix(row: int, col: int, init=None) -> list[list]:
    return [[init] * col for _ in range(row)]
