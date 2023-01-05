class CycleExistError(Exception):
    pass


class DependencyTrees:
    def __init__(self, roots: list):
        self.roots = roots

    def serialize(self) -> list:
        def dfs(node, visited: set, current_path: set, result: list):
            if node in current_path:
                raise CycleExistError(f"{node}")
            if node in visited:
                return
            current_path.add(node)
            visited.add(node)
            result.append(node)
            for child in node.children:
                dfs(child, visited, current_path, result)
            current_path.remove(node)

        result, visited, current_path = list(), set(), set()
        for root in self.roots:
            dfs(root, visited, current_path, result)
        return result


