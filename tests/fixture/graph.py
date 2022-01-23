from ezcode.graph.directed_acyclic_graph import ActivityOnVertexGraph


dependencies = [("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")]
dag = ActivityOnVertexGraph(dependencies)
dag_string = """
  a b c d e f 
a       *     
b           * 
c *         * 
d   *         
e             
f         *   
"""[1:]

non_dag = ActivityOnVertexGraph([("a", "b"), ("b", "a")])