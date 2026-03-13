import networkx as nx

'''
This is a Custom class used to handle graphs in a more dynamic way
inside the Renderer and generally throughout the codebase
'''
class Graph:
    def __init__(self, isDirected=False,name = "Graph",r_a="spring"):
        self.is_directed = isDirected
        self.graph = nx.DiGraph() if isDirected else nx.Graph()
        self.name = name
        self.render_algorithm = r_a
        self.pos = None
        self.nodes = []
        self.edges = []
        self.articulation_points = {}
        self.eccentricity = {}
        self.degrees = {}
        self.node_info = {"node_colors": [], "node_sizes": []}
        self.edge_info = {"edge_colors": [], "edge_widths": []}

    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)
        self.nodes = self.graph.nodes()

    def add_edges(self, edges):
        self.graph.add_edges_from(edges)
        self.edges = self.graph.edges()

    def update(self):
        layout_func = getattr(nx.drawing.layout, self.render_algorithm + "_layout")
        self.pos = layout_func(self.graph.to_undirected())
        nodes = list(self.graph.nodes())
        edges = list(self.graph.edges())
        self.node_info["node_colors"] = [self.graph.nodes[n].get('color', (1, 0, 0)) for n in nodes]
        self.node_info["node_sizes"]  = [self.graph.nodes[n].get('size', 300) for n in nodes]
        self.edge_info["edge_colors"] = [self.graph.edges[e].get('color', (0, 0, 0)) for e in edges]
        self.edge_info["edge_widths"] = [self.graph.edges[e].get('width', 1.0) for e in edges]

    def get_most_important(self,func):
        if func:
            best,best_score = None,0
            for node in self.nodes:
                score = func(self.graph,node)
                if score > best_score:
                    best,best_score = node,score
            return best,best_score
        else:
            print(f"Error,Selected Importance Function does not exist")

    def get_UG_largest_connected_subgraph(self):
        UG = self.graph.to_undirected()
        largest_cc = max(nx.connected_components(UG), key=len)
        UG_connected = UG.subgraph(largest_cc)
        return UG_connected
    # ALL-NODE METHODS
    def get_degrees(self):
        return dict(nx.degree(self.graph))

    def get_articulation_points(self):
        U = self.get_UG_largest_connected_subgraph()
        return set(nx.articulation_points(U))

    def get_eccentricity(self):
        U = self.get_UG_largest_connected_subgraph()
        return dict(nx.eccentricity(U))
    # GET-NODE METHODS
    def get_node_degree(self,node):
        return  self.degrees[node]

    def get_node_articulation_point(self,node):
        return node in self.articulation_points

    def get_node_eccentricity(self,node):
        return self.eccentricity[node]