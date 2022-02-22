from typing import List
from collections import deque
from ezcode.array.heap import PriorityMap
from ezcode.graph import Graph, NegativeCycleExist, PositiveCycleExist, UnweightedGraphExpected


class UndirectedGraph(Graph):
    def __init__(self, edges: List[list] = None, weights: list = None, mark: str = "*"):
        super().__init__(is_weighted=(weights is not None), mark=mark)
        # self.nodes = {node_id, {node_id, weight}}
        if edges:
            self.build(edges=edges, weights=weights)

    def build(self, edges: List[list], weights: list = None):
        if weights is None:
            weights = [1] * len(edges)
        for (n1, n2), weight in zip(edges, weights):
            if n1 is not None and n2 is not None:
                if n1 not in self.nodes:
                    self.nodes[n1] = dict()
                if n2 not in self.nodes:
                    self.nodes[n2] = dict()
                self.nodes[n1][n2] = self.nodes[n2][n1] = weight
            elif n1 is not None:
                if n1 not in self.nodes:
                    self.nodes[n1] = dict()
            elif n2 is not None:
                if n2 not in self.nodes:
                    self.nodes[n2] = dict()
        # For print
        self.sorted_node_ids = sorted(self.nodes.keys())
        self.node_id_index_map = dict()
        for index, node_id in enumerate(self.sorted_node_ids):
            self.node_id_index_map[node_id] = index
            self.cell_size = max(self.cell_size, len(str(node_id)))
        for weight in weights:
            self.cell_size = max(self.cell_size, len(str(weight)))
        self.cell_size += 2  # Add two spaces in between

    def get_weight(self, incoming, outgoing):
        return self.nodes[incoming][outgoing] if outgoing in self.nodes[incoming] else None

    def dfs_path_value(self, src_node_id, dst_node_id, visited = set(), self_loop_value=0, path_value_init=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        if src_node_id == dst_node_id:
            return self_loop_value
        top_path_value = path_value_init
        for node_id, weight in self.nodes[src_node_id].items():
            if node_id not in visited:
                visited.add(node_id)
                path_value = self.dfs_path_value(node_id, dst_node_id, visited, self_loop_value, path_value_init, path_value_func, min_max_func)
                visited.remove(node_id)
                top_path_value = min_max_func(top_path_value, path_value_func(weight, path_value))
        return top_path_value

    def bfs_path_value(self, src_node_id, dst_node_id=None):
        """ Only works for unweighted graph """
        if self.is_weighted:
            raise UnweightedGraphExpected()
        path_values, queue, visited = dict(), deque([src_node_id]), set([src_node_id])
        for node_id in self.nodes.keys():
            path_values[node_id] = 0 if node_id == src_node_id else float("inf")
        while len(queue) > 0:
            node_id = queue.popleft()
            for neighbor_id in self.nodes[node_id].keys():
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
                    path_values[neighbor_id] = path_values[node_id] + 1
                    if dst_node_id is not None and neighbor_id == dst_node_id:
                        return path_values[neighbor_id]
        return path_values[neighbor_id] if dst_node_id is not None else path_values

    def dijkstra(self, src_node_id, self_loop_value=0, path_value_init=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        """ Positive Weight Only: O(V + E*logV). On dense graphs, dijkstra is faster than spfa """
        path_values, visited = dict(), set()
        min_heap = True if min_max_func == min else False
        candidates = PriorityMap({src_node_id:self_loop_value}, min_heap=min_heap)
        for node_id in self.nodes.keys():
            path_values[node_id] = self_loop_value if node_id == src_node_id else path_value_init
        while len(candidates) > 0:
            top_path_value, top_node_id = candidates.pop()
            visited.add(top_node_id)
            for relax_node_id, weight in self.nodes[top_node_id].items():
                if relax_node_id not in visited:
                    path_values[relax_node_id] = min_max_func(path_values[relax_node_id], path_value_func(top_path_value, weight))
                    candidates.push(path_values[relax_node_id], relax_node_id)
        return path_values

    def spfa(self, src_node_id, self_loop_value=0, path_value_init=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min, check_cycle=False):
        """ Improved Bellman Ford Algorithm: can handle Negative Weight and detect Negative Cycle: worst case O(V*E), average O(E), sparse graphs O(V^2) """
        path_values, queue, queue_set = dict(), deque([src_node_id]), set([src_node_id])
        enqueue_counters = dict() if check_cycle else None
        for node_id in self.nodes.keys():
            path_values[node_id] = self_loop_value if node_id == src_node_id else path_value_init
            if check_cycle:
                enqueue_counters[node_id] = 1 if node_id == src_node_id else 0
        while len(queue) > 0:
            node_id = queue.popleft()
            queue_set.remove(node_id)
            for relax_node_id, weight in self.nodes[node_id].items():
                new_path_value = path_value_func(path_values[node_id], weight)
                if (min_max_func == min and new_path_value < path_values[relax_node_id]) or (min_max_func == max and new_path_value > path_values[relax_node_id]):
                    path_values[relax_node_id] = new_path_value
                    if relax_node_id not in queue_set:
                        queue.append(relax_node_id)
                        queue_set.add(relax_node_id)
                        if check_cycle:
                            enqueue_counters[relax_node_id] += 1
                            if enqueue_counters[relax_node_id] > len(self.nodes):
                                if min_max_func == min:
                                    raise NegativeCycleExist()
                                else:
                                    raise PositiveCycleExist()
        return path_values

    def floyd(self, self_loop_value=0, path_value_init=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        """ Can handle Negative Weight but not Negative cycle: O(V^3) """
        all_path_values = dict()  # <node_id, <node_id, path_value>>
        for n1 in self.nodes.keys():
            all_path_values[n1] = dict()
            for n2 in self.nodes.keys():
                if n1 == n2:
                    all_path_values[n1][n2] = self_loop_value
                elif n2 in self.nodes[n1]:
                    all_path_values[n1][n2] = self.nodes[n1][n2]
                else:
                    all_path_values[n1][n2] = path_value_init
        for relax in self.nodes.keys():
            for src in self.nodes.keys():
                for dst in self.nodes.keys():
                    relaxed_path_value = path_value_func(all_path_values[src][relax], all_path_values[relax][dst])
                    all_path_values[src][dst] = min_max_func(all_path_values[src][dst], relaxed_path_value)
        return all_path_values









        
















