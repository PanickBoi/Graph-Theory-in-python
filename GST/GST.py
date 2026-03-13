import os
import networkx as nx
import matplotlib.pyplot as plt
import json

from prompt_toolkit.filters import renderer_height_is_known

from Modules import IAM, PM
from Classes import Graph, Renderer
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
iaa = rules["algorithm"]
render = rules["render"]

lt = sim["layout"]
use_preset = sim["use_preset"]
colormap = np["colormap"]

graph_folder = r"Graphs"

def con_change(con,r): #,con-> is the number of connection for this node,r -> is the random number provided
    f = r*(con+1)
    return

def logging_n_statistics(G):
    # // LOGGING

    best, best_score = None, -sys.maxsize - 1
    node_info = info["node_info"]
    # edge_info = info["edge_info"] //temporarily unused
    if node_info["is_enabled"]:
        for node in G.nodes:
            if node_info["n_label"]: print("//Node", node)
            if node_info["n_degree"]: print("Degree: ", G.get_node_degree(node))
            if node_info["n_eccentricity"] and G.get_node_degree(node) >= 1: print("Eccentricity: ", G.get_node_eccentricity(node))
            if node_info["n_articulation_point"] and G.get_node_degree(node) >= 1: print("Articulation Point?: ", True if G.get_node_articulation_point(node) else False)
            if node_info["n_importance"]["is_enabled"]:
                result = None
                func = getattr(IAM, iaa["choice"])
                if func:
                    result = func(G, node)
                else:
                    print(f"Error,Non-existent Importance Function: {iaa['choice']}")
                print("Importance: ",result)
                if node_info["n_importance"]["show_most_important"]:

                    if result > best_score:
                        best_score = result
                        best = node
            print()
        if node_info["n_importance"]["show_most_important"]:
            print("=========")
            print("Most Important Node: ", best, " with Importance of: ", best_score)
            print("==========")


def paint_nodes(G):
    # ///// PAINTING /////
    if np["is_enabled"]:
        for node in G.nodes:
            func = None
            if colormap["is_enabled"]:
                if colormap["colormap_func"] != "":
                    func = getattr(PM, colormap["colormap_func"])
                else:
                    func = getattr(PM, "colormap")
            else:
                func = getattr(PM, np["choice"])
            if func:
                func(G, node)
            else:
                print(f"Error,Non-existent painting function: {np["choice"]}")

def preset_generation():
    graph_list = os.listdir(graph_folder)
    graph_objects = []
    for graph in graph_list:
        data = json.load(open(graph_folder + "/" + graph))
        G = Graph.Graph(data["directed"],graph,data["algorithm"] if not lt["override"] else lt["algorithm"])
        G.add_nodes(data["V"])
        G.add_edges(data["E"])
        G.articulation_points = G.get_articulation_points()
        G.eccentricity = G.get_eccentricity()
        G.degrees = G.get_degrees()
        graph_objects.append(G)
        paint_nodes(G)
        logging_n_statistics(G)

    # // RENDERING
    renderer = Renderer.Renderer(graph_objects, render["update_type"], render["fps"])
    renderer.start_render()
    renderer.stop_render()

def creation():
    # // CREATION
    if use_preset:
        preset_generation()
    else:
        None #USER-GENERATION

def main(): #LET THERE BE LIGHT.
    creation()

if __name__ == '__main__':
    main()