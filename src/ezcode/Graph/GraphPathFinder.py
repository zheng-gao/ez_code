from collections import deque
from typing import Callable

from ezcode.Graph.UndirectedGraph import UndirectedGraph
from ezcode.Graph.DirectedGraph import DirectedGraph
from ezcode.Heap.PriorityMap import PriorityMap


class NegativeCycleExistError(Exception):
    pass


class UnweightedGraphExpectedError(Exception):
    pass


class GraphPathFinder:
    def __init__(self, graph=None, is_directed: bool = False, edge_weight_dict: dict = None, edges: list[list] = None, weights: list = None):
        if graph is None:
            if is_directed:
                self.graph = DirectedGraph(edge_weight_dict=edge_weight_dict, edges=edges, weights=weights)
            else:
                self.graph = UndirectedGraph(edge_weight_dict=edge_weight_dict, edges=edges, weights=weights)
        else:
            self.graph = graph

    def __str__(self):
        return str(self.graph)

    def print(self):
        print(self.graph)

    """
    Shortest Path Algorithm Summary:
                 Value  S-Paths   Undirected  Directed  Weighted  Negative-Weight  Negative-Loop   Space     Time
    dfs          1:1    no        yes         yes       yes       yes              no              O(V)      O(E)
    bfs          1:N    1         yes         yes       no        no               no              O(V)      O(E)
    backtracking 1:1    all       yes         yes       yes       yes              no              O(V)      O(V!)
    dijkstra     1:N    1         yes         yes       yes       no               no              O(VlogV)  O(V+ElogV) using fabonacci heap, otherwise O(V^2)
    bellman-ford 1:N    1         yes         yes       yes       yes             Find                       O(kE) on sparse graph, O(VE) for dense graph
    spfa         1:N    1         yes         yes       yes       yes            Detect            O(V)      O(VE)
    floyd        N:N    N/A       yes         yes       yes       yes              no              O(V^2)    O(V^3)

    Notes:
    On fixed edge weight (e.g. unweighted graphs, w=1), dijkstra == bfs and both of them can return early
    dijkstra/spfa are good for sparse graph
    on dense graph, dijkstra is faster than spfa
    """
    def path_dict_to_path(self, path_dict: dict, dst_node_id) -> list:
        if dst_node_id not in path_dict:
            return None
        path, parent = deque([dst_node_id]), path_dict[dst_node_id]
        while parent:
            path.appendleft(parent)
            parent = path_dict[parent] if parent in path_dict else None
        return list(path)

    def backtracking(self,
        src_node_id,
        dst_node_id,
        self_loop_weight=0,
        disconnected_edge_weight=float("inf"),
        path_value_func: Callable = lambda a, b: a + b,
        is_min: bool = True
    ):
        def _backtracking(node_id, path_value, current_path: list, visited: set, best_paths: list):
            """ O(V!) """
            if node_id == dst_node_id:
                if (is_min and path_value < best_paths[0]) or (not is_min and path_value > best_paths[0]):
                    best_paths[0] = path_value
                    best_paths[1].clear()
                    best_paths[1].append(current_path.copy())
                elif path_value == best_paths[0]:
                    best_paths[1].append(current_path.copy())
            else:
                for neighbor_id, weight in self.graph.get_edges(node_id=node_id, is_outgoing=True).items():
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        current_path.append(neighbor_id)
                        _backtracking(neighbor_id, path_value_func(path_value, weight), current_path, visited, best_paths)
                        current_path.pop()
                        visited.remove(neighbor_id)

        current_path, visited, best_paths = list([src_node_id]), set([src_node_id]), list([disconnected_edge_weight, list()])
        _backtracking(src_node_id, self_loop_weight, current_path, visited, best_paths)
        return best_paths[0], best_paths[1]  # value, paths

    def bfs(self, src_node_id, dst_node_id=None):
        """ O(E): Only works for unweighted graph """
        if self.graph.is_weighted:
            raise UnweightedGraphExpectedError("bfs algorithm only works for unweighted graph")
        if src_node_id is not None and src_node_id == dst_node_id:
            return 0, list([src_node_id])
        path_values, path_dict, queue, visited = dict(), dict(), deque([src_node_id]), set([src_node_id])
        for node_id in self.graph.nodes.keys():
            path_values[node_id] = 0 if node_id == src_node_id else float("inf")
        while len(queue) > 0:
            node_id = queue.popleft()
            for neighbor_id in self.graph.get_edges(node_id=node_id, is_outgoing=True).keys():
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
                    path_values[neighbor_id] = path_values[node_id] + 1
                    path_dict[neighbor_id] = node_id
                    if dst_node_id is not None and neighbor_id == dst_node_id:  # return early if the destination node is given
                        return path_values[dst_node_id], self.path_dict_to_path(path_dict, dst_node_id)
        return None, path_values

    def dijkstra(self,
        src_node_id,
        dst_node_id=None,
        self_loop_weight=0,
        disconnected_edge_weight=float("inf"),
        path_value_func: Callable = lambda a, b: a + b,
        is_min: bool = True
    ):
        """ Positive Weight Only: O(V + E*logV). On dense graphs, dijkstra is faster than spfa """
        if src_node_id is not None and src_node_id == dst_node_id:
            return self_loop_weight, list([src_node_id])
        path_values, path_dict, visited = dict(), dict(), set()
        candidates = PriorityMap({src_node_id: self_loop_weight}, min_heap=is_min)
        for node_id in self.graph.nodes.keys():
            path_values[node_id] = self_loop_weight if node_id == src_node_id else disconnected_edge_weight
        while len(candidates) > 0:
            best_node_id, best_path_value = candidates.pop(with_priority=True)
            visited.add(best_node_id)
            for relaxed_node_id, weight in self.graph.get_edges(node_id=best_node_id, is_outgoing=True).items():
                if relaxed_node_id not in visited:
                    new_path_value = path_value_func(best_path_value, weight)
                    if (is_min and new_path_value < path_values[relaxed_node_id]) or (not is_min and new_path_value > path_values[relaxed_node_id]):
                        path_values[relaxed_node_id] = new_path_value
                        path_dict[relaxed_node_id] = best_node_id
                    candidates.push(item=relaxed_node_id, priority=path_values[relaxed_node_id])
        if dst_node_id is None:
            return None, path_values
        return path_values[dst_node_id], self.path_dict_to_path(path_dict, dst_node_id)

    def spfa(self,
        src_node_id,
        dst_node_id=None,
        self_loop_weight=0,
        disconnected_edge_weight=float("inf"),
        path_value_func: Callable = lambda a, b: a + b,
        is_min: bool = True,
        check_cycle=False
    ):
        """ Improved Bellman Ford Algorithm: can handle Negative Weight and detect Negative Cycle: worst case O(V*E), sparse graphs O(kE), dense graph O(VE) """
        if src_node_id is not None and src_node_id == dst_node_id:
            return self_loop_weight, list([src_node_id])
        path_values, path_dict, queue, queue_set = dict(), dict(), deque([src_node_id]), set([src_node_id])
        enqueue_counters = dict() if check_cycle else None
        for node_id in self.graph.nodes.keys():
            path_values[node_id] = self_loop_weight if node_id == src_node_id else disconnected_edge_weight
            if check_cycle:
                enqueue_counters[node_id] = 1 if node_id == src_node_id else 0
        while len(queue) > 0:
            node_id = queue.popleft()
            queue_set.remove(node_id)
            for relaxed_node_id, weight in self.graph.get_edges(node_id=node_id, is_outgoing=True).items():
                new_path_value = path_value_func(path_values[node_id], weight)
                if (is_min and new_path_value < path_values[relaxed_node_id]) or (not is_min and new_path_value > path_values[relaxed_node_id]):
                    path_values[relaxed_node_id] = new_path_value
                    if path_dict is not None:
                        path_dict[relaxed_node_id] = node_id
                    if relaxed_node_id not in queue_set:
                        queue.append(relaxed_node_id)
                        queue_set.add(relaxed_node_id)
                        if check_cycle:
                            enqueue_counters[relaxed_node_id] += 1
                            if enqueue_counters[relaxed_node_id] > len(self.graph.nodes):
                                raise NegativeCycleExistError()
        if dst_node_id is None:
            return None, path_values
        return path_values[dst_node_id], self.path_dict_to_path(path_dict, dst_node_id)

    def floyd(self,
        self_loop_weight=0,
        disconnected_edge_weight=float("inf"),
        path_value_func: Callable = lambda a, b: a + b,
        is_min: bool = True
    ):
        """ Can handle Negative Weight but not Negative cycle: O(V^3) """
        adjacent_matrix = dict()  # <node_id, <node_id, path_value>>
        for n1 in self.graph.nodes.keys():
            adjacent_matrix[n1] = dict()
            for n2 in self.graph.nodes.keys():
                if n1 == n2:
                    adjacent_matrix[n1][n2] = self_loop_weight
                elif n2 in self.graph.get_edges(node_id=n1, is_outgoing=True):
                    adjacent_matrix[n1][n2] = self.graph.get_weight(n1, n2, is_outgoing=True)
                else:
                    adjacent_matrix[n1][n2] = disconnected_edge_weight
        for relax in self.graph.nodes.keys():  # relax must be at the first loop, src and dst loops can swap.
            for src in self.graph.nodes.keys():
                for dst in self.graph.nodes.keys():
                    relaxed_path_value = path_value_func(adjacent_matrix[src][relax], adjacent_matrix[relax][dst])
                    if (is_min and relaxed_path_value < adjacent_matrix[src][dst]) or (not is_min and relaxed_path_value > adjacent_matrix[src][dst]):
                        adjacent_matrix[src][dst] = relaxed_path_value
        return adjacent_matrix





