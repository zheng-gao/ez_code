class DisjointSets:
    def __init__(self, nodes: set):
        self.parents = dict()
        self.tree_ranks = dict()  # Do not use tree heights, calculate height is O(N), disjon method will break the ranks
        self.tree_sizes = dict()
        for node in nodes:
            self.parents[node] = node
            self.tree_sizes[node] = 1
            self.tree_ranks[node] = 1
        self.number_of_disjoint_sets = len(nodes)

    def __len__(self):
        return self.number_of_disjoint_sets

    def union(self, node1, node2):
        parent1, parent2 = self.find(node1), self.find(node2)
        if parent1 != parent2:
            if self.tree_ranks[parent1] < self.tree_ranks[parent2]:
                parent1, parent2 = parent2, parent1
            if self.tree_ranks[parent1] == self.tree_ranks[parent2]:
                self.tree_ranks[parent1] += 1
            # if self.tree_sizes[parent1] < self.tree_sizes[parent2]:
            #     parent1, parent2 = parent2, parent1
            self.parents[parent2] = parent1
            self.tree_sizes[parent1] += self.tree_sizes[parent2]
            self.number_of_disjoint_sets -= 1

    def find(self, node):
        """ O(logN) on average """
        if node in self.parents:
            return node if self.parents[node] == node else self.find(self.parents[node])
        raise ValueError(f"Node \"{node}\" not found in disjoint sets")

    def is_joint(self, node1, node2):
        return self.find(node1) == self.find(node2)

    def get_set_size(self, node):
        return self.tree_sizes[self.find(node)]

    # def disjoin(self, node):
    #     parent = self.find(node)
    #     if parent != node:
    #         self.parents[node] = node
    #         self.tree_sizes[parent] -= self.tree_sizes[node]
    #         self.number_of_disjoint_sets += 1





