from collections import Counter

from ezcode.Math import approximately_equals
from ezcode.Random.RandomIndex import RandomIndexArray, RandomIndexTree


def test_random_weighted_index():
    def _test(random_index_generator, weights):
        error, samples_size, counter = 0.3, 1000, Counter()
        for _ in range(samples_size):
            counter.update([random_index_generator.random_index()])
        sum_weights = sum(weights)
        for index, weight in enumerate(weights):
            assert approximately_equals(target=(samples_size * weight / sum_weights), error=error, value=counter[index])
        weights[1], counter = 1, Counter()
        random_index_generator.update(index=1, weight=1)
        sum_weights = sum(weights)
        for _ in range(samples_size):
            counter.update([random_index_generator.random_index()])
        for index, weight in enumerate(weights):
            assert approximately_equals(target=(samples_size * weight / sum_weights), error=error, value=counter[index])
    
    weights = [1, 2, 3, 4]
    _test(RandomIndexArray(weights), weights)
    _test(RandomIndexTree(weights), weights)
