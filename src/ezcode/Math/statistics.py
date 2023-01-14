import random


class RandomGenerator:
    def __init__(self, weights: list):
        self.sum, self.cumulative_sum = 0, list()
        for weight in weights:
            self.sum += weight
            self.cumulative_sum.append(self.sum)

    def random_index(self) -> int:
        r = random.random() * self.sum
        start, end = 0, len(self.cumulative_sum) - 1
        while start < end:
            mid = start + (end - start) // 2
            if r < self.cumulative_sum[mid]:
                end = mid
            else:
                start = mid + 1
        return start


