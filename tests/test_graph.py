from ezcode.array.utils import is_copied
from fixture.graph import dag, dag_string, non_dag


def test_graph_string():
    assert str(dag) == dag_string


def test_topological_order():
    assert is_copied(dag.topological_order(), ["e", "b", "d", "a", "c"])


def test_is_directed_acyclic_graph():
    assert dag.is_directed_acyclic_graph()
    assert not non_dag.is_directed_acyclic_graph()

