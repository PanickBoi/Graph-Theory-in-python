import networkx as nx
from matplotlib import cm
import json
import IAM
'''
Painting Module

here you add your own functions to paint nodes
'''

rules = json.load(open('rules.json'))
painting = rules["node_painting"]


def default(G,node): #Default algorithm for painting nodes
    if painting["color"]:
        r, g, b = 50, 50, 50 #0-255
        c = (r / 255, g / 255, b / 255)# 0-1
        G.nodes[node]["color"] = c

    if painting["resize"]:
        size = 4
        G.nodes[node]["size"] = size

def colormap(G, node): #Default colormap algorithm
    cm_json = painting["colormap"]
    cmap = getattr(cm, cm_json["colormap_func"], cm.YlOrRd)
    map_by = cm_json["map_by"]

    if map_by == "degree":
        values = dict(G.degree())
    elif map_by == "eccentricity":
        UG = G.to_undirected()
        largest_cc = max(nx.connected_components(UG), key=len)
        UG_connected = UG.subgraph(largest_cc)
        ecc = nx.eccentricity(UG_connected)
        values = {n: ecc.get(n, 0) for n in G.nodes()}
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