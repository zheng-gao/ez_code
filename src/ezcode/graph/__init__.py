from collections import deque
from ezcode.heap import PriorityMap


class NegativeCycleExist(Exception):
    pass


class PositiveCycleExist(Exception):
    pass


class UnweightedGraphExpected(Exception):
    pass


class Graph:
    def __init__(self, is_weighted: bool, mark: str = "*"):
        self.nodes = dict()
        self.is_weighted: bool = is_weighted
        self.sorted_node_ids: list = None     # for print
        self.node_id_index_map: dict = None   # for print
        self.mark = mark                      # for print
        self.cell_size = 1                    # for print

    def __len__(self) -> int:
        return len(self.nodes)

    def _cell(self, item=None) -> str:
        if not self.is_weighted and item == 1:
            item = self.mark
        if item is None:
            item = ""
        return str(item) + (" " * (self.cell_size - len(str(item))))

    def get_weight(self, node_id_1, node_id_2, is_outgoing: bool = True):
        edges = self.get_edges(node_id_1, is_outgoing)
        return edges[node_id_2] if node_id_2 in edges else None

    def get_edges(self, node_id, is_outgoing: bool = True):
        pass

    def __str__(self):
        output = self._cell()
        for node_id in self.sorted_node_ids:
            output += self._cell(node_id)
        output += "\n"
        for row in range(len(self)):
            incoming = self.sorted_node_ids[row]
            output += self._cell(incoming)
            for col in range(len(self)):
                outgoing = self.sorted_node_ids[col]
                output += self._cell(self.get_weight(incoming, outgoing))
            output += "\n"
        return output

    def print(self):
        print(self, end="")

    """
    Shortest Path Algorithm Summary:
                      Undirected  Directed  Weighted  Negative Weight  Negative Loop  Topology   Space      Time
    dfs                   yes       yes       yes        yes              no           1 to 1     O(V)      O(V!)
    bfs                   yes       yes       no         no               no           1 to N     O(V)      O(E)
    dijkstra              yes       yes       yes        no               no           1 to N     O(VlogV)  O(V+ElogV) using fabonacci heap, otherwise O(V^2)
    bellman-ford          yes       yes       yes        yes             Find          1 to N               O(kE) on sparse graph, O(VE) for dense graph
    spfa                  yes       yes       yes        yes            Detect         1 to N     O(V)      O(VE)
    floyd                 yes       yes       yes        yes              no           N to N     O(V^2)    O(V^3)

    Notes:
    dijkstra/spfa are good for sparse graph
    on dense graph, dijkstra is faster than spfa
    """

    def dfs_path_value(self, src_node_id, dst_node_id, visited=set(), self_loop_weight=0, disconnected_edge_weight=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        """ O(V!) """
        if src_node_id == dst_node_id:
            return self_loop_weight
        top_path_value = disconnected_edge_weight
        for node_id, weight in self.get_edges(node_id=src_node_id, is_outgoing=True).items():
            if node_id not in visited:
                visited.add(node_id)
                path_value = self.dfs_path_value(node_id, dst_node_id, visited, self_loop_weight, disconnected_edge_weight, path_value_func, min_max_func)
                visited.remove(node_id)
                top_path_value = min_max_func(top_path_value, path_value_func(weight, path_value))
        return top_path_value

    def bfs_path_value(self, src_node_id, dst_node_id=None):
        """ O(E): Only works for unweighted graph """
        if self.is_weighted:
            raise UnweightedGraphExpected()
        path_values, queue, visited = dict(), deque([src_node_id]), set([src_node_id])
        for node_id in self.nodes.keys():
            path_values[node_id] = 0 if node_id == src_node_id else float("inf")
        while len(queue) > 0:
            node_id = queue.popleft()
            for neighbor_id in self.get_edges(node_id=node_id, is_outgoing=True).keys():
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
                    path_values[neighbor_id] = path_values[node_id] + 1
                    if dst_node_id is not None and neighbor_id == dst_node_id:  # return early if the destination node is given
                        return path_values[neighbor_id]
        return path_values[neighbor_id] if dst_node_id is not None else path_values

    def dijkstra(self, src_node_id, self_loop_weight=0, disconnected_edge_weight=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        """ Positive Weight Only: O(V + E*logV). On dense graphs, dijkstra is faster than spfa """
        path_values, visited = dict(), set()
        min_heap = True if min_max_func == min else False
        candidates = PriorityMap({src_node_id: self_loop_weight}, min_heap=min_heap)
        for node_id in self.nodes.keys():
            path_values[node_id] = self_loop_weight if node_id == src_node_id else disconnected_edge_weight
        while len(candidates) > 0:
            top_path_value, top_node_id = candidates.pop()
            visited.add(top_node_id)
            for relax_node_id, weight in self.get_edges(node_id=top_node_id, is_outgoing=True).items():
                if relax_node_id not in visited:
                    path_values[relax_node_id] = min_max_func(path_values[relax_node_id], path_value_func(top_path_value, weight))
                    candidates.push(path_values[relax_node_id], relax_node_id)
        return path_values

    def spfa(self, src_node_id, self_loop_weight=0, disconnected_edge_weight=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min, check_cycle=False):
        """ Improved Bellman Ford Algorithm: can handle Negative Weight and detect Negative Cycle: worst case O(V*E), sparse graphs O(kE), dense graph O(VE) """
        path_values, queue, queue_set = dict(), deque([src_node_id]), set([src_node_id])
        enqueue_counters = dict() if check_cycle else None
        for node_id in self.nodes.keys():
            path_values[node_id] = self_loop_weight if node_id == src_node_id else disconnected_edge_weight
            if check_cycle:
                enqueue_counters[node_id] = 1 if node_id == src_node_id else 0
        while len(queue) > 0:
            node_id = queue.popleft()
            queue_set.remove(node_id)
            for relax_node_id, weight in self.get_edges(node_id=node_id, is_outgoing=True).items():
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

    def floyd(self, self_loop_weight=0, disconnected_edge_weight=float("inf"), path_value_func=lambda a, b: a + b, min_max_func=min):
        """ Can handle Negative Weight but not Negative cycle: O(V^3) """
        adjacent_matrix = dict()  # <node_id, <node_id, path_value>>
        for n1 in self.nodes.keys():
            adjacent_matrix[n1] = dict()
            for n2 in self.nodes.keys():
                if n1 == n2:
                    adjacent_matrix[n1][n2] = self_loop_weight
                elif n2 in self.get_edges(node_id=n1, is_outgoing=True):
                    adjacent_matrix[n1][n2] = self.get_weight(n1, n2, is_outgoing=True)
                else:
                    adjacent_matrix[n1][n2] = disconnected_edge_weight
        for relax in self.nodes.keys():  # relax must be at the first loop, src and dst loops can swap.
            for src in self.nodes.keys():
                for dst in self.nodes.keys():
                    relaxed_path_value = path_value_func(adjacent_matrix[src][relax], adjacent_matrix[relax][dst])
                    adjacent_matrix[src][dst] = min_max_func(adjacent_matrix[src][dst], relaxed_path_value)
        return adjacent_matrix



