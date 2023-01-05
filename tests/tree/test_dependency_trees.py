from ezcode.tree.dependency_trees import DependencyTrees, CycleExistError


def test_dependency_trees():
    class Node:
        def __init__(self, name):
            self.name = name
            self.children = set()

        def add(self, node):
            self.children.add(node)
            return self

    n = [Node(0), Node(1), Node(2), Node(3), Node(4), Node(5)]
    n[1].add(n[0])
    n[2].add(n[0]).add(n[1])
    n[3].add(n[4])
    n[4].add(n[1]).add(n[5])
    n[5].add(n[0]).add(n[2])
    dt = DependencyTrees(n)
    assert dt.serialize() == n
    n[2].add(n[4])
    try:
        dt.serialize()
        assert False
    except CycleExistError:
        assert True