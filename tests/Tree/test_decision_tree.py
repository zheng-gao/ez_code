from ezcode.Tree.DecisionTree import DecisionTree


def test_decision_tree():
    t = DecisionTree()
    l, r = t.split_node(node=t.root, signal="X1", constant=3)
    ll, lr = t.split_node(node=l, signal="X2", constant=1, left_decision="N", right_decision="Y")
    rl, rr = t.split_node(node=r, signal="X1", constant=6, left_decision="N")
    rrl, rrr = t.split_node(node=rr, signal="X3", constant=2, left_decision="Y", right_decision="N")
    assert "Y" == t.evaluate({"X1": 2, "X2": 1, "X3": 11})
    assert "N" == t.evaluate({"X1": 8, "X2": 4, "X3": 12})
    assert str(t) == """
          ┌──────────────(X1|3)───────────────┐              
 ┌─────(X2|1)──────┐                 ┌─────(X1|6)──────┐     
(N)               (Y)               (N)           ┌─(X3|2)─┐ 
                                                 (Y)      (N)
"""[1:]
