import networkx as nx
import matplotlib.pyplot as plt
import random
import json
import IAM #// Importance Algorithms
import PM #// Painting Module
import sys
# Graph Simulation Tool (GST)

# by PanickBoi
# https://github.com/PanickBoi

#///// INITIALIZATION /////
rules = json.load(open('rules.json'))
print(rules)
np = rules["node_painting"]
sim = rules["simulation"]
info = rules["graph_info"]
algorithm = rules["algorithm"]

lt = sim["layout"]
up = sim["use_preset"]
colormap = np["colormap"]



def con_change(con,r): #,con-> is the number of connection for this node,r -> is the random number provided
    f = r*(con+1)
    return

def main():
    G = None
    pos = None
    if up["is_enabled"]:
        # ///// CREATION /////
        for G_json in up["file_names"]:
            plt.figure(num=G_json,dpi=100)
            data = json.load(open(G_json+".json"))
            G = nx.DiGraph() if data["directed"] else nx.Graph()
            G.add_nodes_from(data["V"])
            G.add_edges_from(data["E"])
            algo = lt["algorithm"] if lt["override"] else data["algorithm"]
            func = getattr(nx.drawing.layout,algo+"_layout")
            if func:
                pos = func(G.to_undirected())
            else:
                print(f"Error,Non-existent layout function: {np["choice"]}")
            UG = G.to_undirected()
            best, best_score = None, -sys.maxsize - 1
            # ///// PAINTING /////
            for node in G.nodes():
                if np["is_enabled"]:
                    func = None
                    if colormap["is_enabled"]:
                        if colormap["colormap_func"]:
                            func = getattr(PM, colormap["colormap_func"])
                        else:
                            func = getattr(PM, "colormap")
                    else:
                        func = getattr(PM, np["choice"])
                    if func:
                        func(G,node)
                    else:
                        print(f"Error,Non-existent painting function: {np["choice"]}")
                #///// DISPLAY /////
                if info["is_enabled"]:
                    node_info = info["node_info"]
                    edge_info = info["edge_info"]
                    if node_info["is_enabled"]:
                        largest_cc = max(nx.connected_components(UG), key=len)
                        UG_connected = UG.subgraph(largest_cc)
                        ecc = nx.eccentricity(UG_connected)
                        a_p = set(nx.articulation_points(UG_connected))
                        if node_info["n_label"]: print("//Node", node)
                        if node_info["n_degree"]: print("Degree: ",G.degree(node))
                        if node_info["n_eccentricity"] and G.degree(node) >= 1: print("Eccentricity: ",ecc[node])
                        if node_info["n_articulation_point"]: print("Articulation Point?: ",True if node in a_p else False)
                        if node_info["n_importance"]["is_enabled"]:
                            result = None
                            func = getattr(IAM, algorithm["choice"])
                            if func:
                                result = func(G,node)
                                print("Importance: ",result)
                            else:
                                print(f"Error,Non-existent importance-algorithm function: {algo["choice"]}")
                            if node_info["n_importance"]["show_most_important"]:
                                if result > best_score:
                                    best_score = result
                                    best = node
                        print()
                    if node_info["n_importance"]["show_most_important"]:
                        print("=========")
                        print("Most Important Node: ",best," with Importance of: ",best_score)
                        print("==========")

            if pos is not None:
                node_colors = [G.nodes[n].get('color', (1, 0, 0)) for n in G.nodes()]  # default red
                node_sizes = [G.nodes[n].get('size', 5) * 50 for n in G.nodes()]
                nx.draw_networkx(G,pos,node_color=node_colors,node_size=node_sizes)
            else:
                print("Error,No Position Layout given..")
        plt.show()



if __name__ == '__main__':
    main()