
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

    def get_weight(self, incoming, outgoing):
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
