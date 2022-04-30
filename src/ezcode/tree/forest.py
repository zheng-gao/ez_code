class DisjointSets:
    def __init__(self, nodes: set):
        self.parents = dict()
        self.tree_roots = set()
        self.tree_ranks = dict()  # Do not use tree heights, calculate height is O(N)
        self.tree_sizes = dict()
        for node in nodes:
            self.parents[node] = node
            self.tree_roots.add(node)
            self.tree_sizes[node] = 1
            self.tree_ranks[node] = 1
        self.number_of_disjoint_sets = len(nodes)

    def __len__(self):
        return self.number_of_disjoint_sets

    def union(self, node1, node2):
        """
            O(log*N), amortized O(1)
            return: True merged, False already in the same set
        """
        parent1, parent2 = self.find(node1), self.find(node2)
        if parent1 != parent2:
            if self.tree_ranks[parent1] < self.tree_ranks[parent2]:
                parent1, parent2 = parent2, parent1
            if self.tree_ranks[parent1] == self.tree_ranks[parent2]:
                self.tree_ranks[parent1] += 1
            self.parents[parent2] = parent1
            self.tree_roots.remove(parent2)
            self.tree_sizes[parent1] += self.tree_sizes[parent2]
            self.number_of_disjoint_sets -= 1
            return True
        return False

    def find(self, node):
        """ O(log*N), amortized O(1) """
        if node in self.parents:
            path_compression = list()
            while node != self.parents[node]:
                node = self.parents[node]
                path_compression.append(node)
            for n in path_compression:
                if n != node:
                    self.parents[n] = node
                    if n in self.tree_roots:
                        self.tree_roots.remove(n)
            return node
        raise ValueError(f"Node \"{node}\" not found in disjoint sets")

    def is_joint(self, node1, node2):
        return self.find(node1) == self.find(node2)

    def get_set_size(self, node):
        return self.tree_sizes[self.find(node)]

    def get_max_set_size(self):
        max_size = 0
        for root in self.tree_roots:
            max_size = max(max_size, self.get_set_size(root))
        return max_size



