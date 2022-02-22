from ezcode.graph.directed import DirectedGraph


dependencies = [("c", "a"), ("b", "f"), ("e", None), ("a", "d"), ("c", "f"), ("d", "b"), ("f", "e")]
dag = DirectedGraph(edges=dependencies)
dag_string = """
   a  b  c  d  e  f  
a           *        
b                 *  
c  *              *  
d     *              
e                    
f              *     
"""[1:]

non_dag = DirectedGraph(edges=[("a", "b"), ("b", "a")])