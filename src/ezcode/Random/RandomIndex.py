from random import random

from ezcode.Tree.SegmentTree import SegmentTree


class RandomIndex:
    def update(self, index: int, weight):
        pass

    def random_index(self, index: int, weight):
        pass


class RandomIndexArray(RandomIndex):
    def __init__(self, weights: list):
        """ build cumulative_sum: O(N) """
        self.weights = weights.copy()  # Save the weights only when update is required
        self.sum = 0
        self.cumulative_sum = list()
        for weight in weights:
            self.sum += weight
            self.cumulative_sum.append(self.sum)

    def update(self, index: int, weight):
        """ Time: O(N) """
        weight_diff = weight - self.weights[index]
        self.weights[index] = weight
        self.sum += weight_diff
        for i in range(index, len(self.cumulative_sum)):
            self.cumulative_sum[i] += weight_diff

    def random_index(self) -> int:
        """ Time: O(logN) """
        r = random() * self.sum  # random() -> [0, 1)
        start, end = 0, len(self.cumulative_sum) - 1
        while start < end:
            mid = start + (end - start) // 2
            if r < self.cumulative_sum[mid]:
                end = mid
            else:
                start = mid + 1
        return start


class RandomIndexTree(RandomIndex):
    def __init__(self, weights: list):
        """ build tree time: O(N) """
        self.segment_tree = SegmentTree(data_list=weights, merge=lambda x, y: x + y)

    def update(self, index: int, weight):
        """ Time: O(logN) """
        self.segment_tree.update(index, weight)

    def random_index(self):
        """ Time: O(logN) """
        node = self.segment_tree.root
        while node.left is not None:  # Segment Tree is Complete
            if node.right is None:
                node = node.left
            else:  # [0.0, node.data)
                node = node.left if random() * node.data < node.left.data else node.right
        return node.start





