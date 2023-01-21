from ezcode.Tree.BinaryTree import BinaryTree


class DecisionTree(BinaryTree):
    def __init__(self):
        super().__init__(data_name="decision", left_name="left", right_name="right")
        self.root = self.new_node(decision=True, is_leaf=True)

    def new_node(self, decision=None, left=None, right=None, signal=None, constant=None, is_leaf=True):
        node = super().new_node(data=decision, left=left, right=right)
        node.__dict__.update({"signal": signal, "constant": constant, "is_leaf": is_leaf})
        return node

    def node_to_string(self, node) -> str:
        return f"{str(node.signal) + '|' + str(node.constant) if node.decision is None else node.decision}"

    def split_node(self, node, signal, constant, left_decision=None, right_decision=None):
        node.decision = None
        node.signal = signal
        node.constant = constant
        node.left = self.new_node(left_decision)
        node.right = self.new_node(right_decision)
        node.is_leaf = False
        return node.left, node.right

    def update_node(self, node, decision):
        node.decision = decision
        node.is_leaf = True

    def evaluate(self, signals: dict):
        node = self.root
        while not node.is_leaf:
            if signals[node.signal] < node.constant:
                node = node.left
            else:
                node = node.right
        return node.decision
