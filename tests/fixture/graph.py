from ezcode.graph.directed_acyclic_graph import ActivityOnVertexGraph


dependencies = [("c", "a"), ("b", "e"), ("a", "d"), ("c", "e"), ("d", "b")]
dag = ActivityOnVertexGraph(dependencies)
dag_string = """
  a b c d e 
a       *   
b         * 
c *       * 
d   *       
e           
"""[1:]

non_dag = ActivityOnVertexGraph([("a", "b"), ("b", "a")])