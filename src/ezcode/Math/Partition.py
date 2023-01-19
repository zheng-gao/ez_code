

def partitions(items: list) -> list:
    """
        [1, 2, 3, 4]
        =>
        [
            [[1, 2, 3, 4]],
            [[1], [2, 3, 4]],
            [[1], [2], [3, 4]],
            [[1], [2], [3], [4]],
            [[1], [2, 3], [4]],
            [[1, 2], [3, 4]],
            [[1, 2], [3], [4]],
            [[1, 2, 3], [4]]
        ]
    """
    return list(partition_generator(items))


def partition_generator(items: list):
    yield [items]
    for i in range(1, len(items)):
        for parts in partition_generator(items[i:]):
            yield [items[0:i]] + parts

