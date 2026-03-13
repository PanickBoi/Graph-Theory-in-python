import os
import networkx as nx
import json
from Classes import Graph
from networkx.algorithms.bridges import bridges
'''
Importance Algorithms Module (IAM)

- You can import here algorithms (or code your own) that 
 attempt to solve this problem or you own (for ex. finding the most influential people in a community,seeing which power lines are most vital, etc.)
'''


rules_path = os.path.join(os.path.dirname(__file__), '..', 'rules.json')
rules = json.load(open(rules_path))
scoring = rules["algorithm"]["scoring"]

def panicks(G,node):
    '''
    takes all the nodes of the graph then ranks them based upon some factors:
        -the degree of a node
        -the eccentricity of a node
        -the amount of bridge-edges of a node
        -and if a node is an articulation point

    I believe my attempt is a more general appoach to the importance problem

    note: i have discovered that graphs with lower highest-importance nodes are
    harder to 'break' by cutting nodes & bridges

    note 2: Directed graphs are a pain to analyze for importance but i have found a workaround
    '''
    score = 0
    edges = list(G.edges(node))
    degree = G.get_node_degree(node) * scoring["per_degree"]
    ecc = 0

    #Eccentricity calculation,with guard rails in-case of lone nodes
    try:
        ecc = G.get_node_eccentricity(node) * scoring["per_eccentricity"]
    except:
        ecc = len(list(G.nodes()))

    if G.is_directed:
        incoming = len(list(G.graph.predecessors(node)))
        outgoing = len(list(G.graph.successors(node)))
        if outgoing > 0:
            connection_ratio = incoming/outgoing
        else:
            connection_ratio = 0
        score += max(connection_ratio,1)*scoring["per_bridge"]

    else:
        bridges = set(nx.bridges(G.graph))
        for edge in edges:
            score += scoring["per_bridge"] if edge in bridges else 0
        score += scoring["articulation_point"] if G.get_node_articulation_point(node) else 0
    score += degree - ecc
    return score




