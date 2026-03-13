import os
import networkx as nx
from matplotlib import cm
import json
from . import IAM
from Classes import Graph
'''
Painting Module

here you add your own functions to paint nodes
'''

rules_path = os.path.join(os.path.dirname(__file__), '..', 'rules.json')
rules = json.load(open(rules_path))
painting = rules["node_painting"]


def default(G,node): #Default algorithm for painting nodes
    if painting["color"]:
        r, g, b = 50, 50, 50 #0-255
        c = (r / 255, g / 255, b / 255)# 0-1
        G.nodes[node]["color"] = c

    if painting["resize"]:
        size = 4
        G.nodes[node]["size"] = size

def colormap(G, node): #Default node colormap algorithm
    cm_json = painting["colormap"]
    cmap = getattr(cm, cm_json["colormap_func"], cm.YlOrRd)
    map_by = cm_json["map_by"]
    values = None
    if map_by == "degree":
        G.get_degrees()
        values = G.degrees
    elif map_by == "eccentricity":
        G.get_eccentricity()
        values = G.eccentricity
    elif map_by == "importance":
        values = {n: getattr(IAM, rules["algorithm"]["choice"])(G, n) for n in G.nodes()}

    max_val = max(values.values()) if values else 1
    min_val = min(values.values()) if values else 0
    span = (max_val - min_val) if (max_val - min_val) > 0 else 1
    normalized = (values[node] - min_val) / span
    r, g, b, _ = cmap(normalized)
    G.nodes[node]["color"] = (r, g, b)
    if not hasattr(G, '_colormap_cache'):
        G._colormap_cache = {}
    if map_by not in G._colormap_cache:
        G._colormap_cache[map_by] = values
    else:
        values = G._colormap_cache[map_by]