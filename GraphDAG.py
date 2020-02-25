# GraphDAG.py


class GraphDAG:
    def __init__(self,project_name,project_id,project_path):
        from graphviz import Digraph
        self.project = '/'.join([project_path,project_name,'DAG',project_name])
        self.dot = Digraph(name=self.project, format="png")
        
    def add_node(self,node_name):
        self.dot.node(node_name)

    def add_edge(self,A_node,B_node,edge_label=None):
        self.dot.edge(A_node,B_node,label=edge_label)

    def dot_render(self):
        self.dot.render(filename=self.project)