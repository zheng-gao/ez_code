import random


class RandomGenerator:
    def __init__(self, weights: list):
        self.sum = 0
        self.stairs = list()
        for weight in weights:
            self.sum += weight
            self.stairs.append(self.sum)

    def random_index(self) -> int:
        r = random.random() * self.sum
        begin, end = 0, len(self.stairs) - 1
        while begin < end:
            mid = begin + (end - begin) // 2
            if r < self.stairs[mid]:
                end = mid
            else:
                begin = mid + 1
        return begin


