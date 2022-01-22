from ezcode.array.utils import is_copied
from fixture.graph import dag, dag_print, non_dag


def test_graph_to_string():
    assert dag.to_string() == dag_print


def test_topological_order():
    assert is_copied(dag.topological_order(), ["e", "b", "d", "a", "c"])


def test_is_directed_acyclic_graph():
    assert dag.is_directed_acyclic_graph()
    assert not non_dag.is_directed_acyclic_graph()

