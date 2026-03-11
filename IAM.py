import networkx as nx
import json

from networkx.algorithms.bridges import bridges
'''
Importance Algorithms Module (IAM)

- You can import here algorithms (or code your own) that 
 attempt to solve this problem or you own (for ex. finding the most influential people in a community,seeing which power lines are most vital, etc.)
'''


rules = json.load(open('rules.json'))
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
    degree = G.degree(node) * scoring["per_degree"]
    ecc = 0

    #Eccentricity calculation,with guard rails in-case of lone nodes
    UG = G.to_undirected()
    largest_cc = max(nx.connected_components(UG), key=len)
    UG_connected = UG.subgraph(largest_cc)
    try:
        ecc = nx.eccentricity(UG_connected)[node] * scoring["per_eccentricity"]
    except:
        ecc = len(list(G.nodes()))

    if G.is_directed():
        incoming = len(list(G.predecessors(node)))
        outgoing = len(list(G.successors(node)))
        if outgoing > 0:
            connection_ratio = incoming/outgoing
        else:
            connection_ratio = 0
        score += max(connection_ratio,1)*scoring["per_bridge"]

    else:
        bridges = set(nx.bridges(G))
        artic_points = set(nx.articulation_points(G))
        for edge in edges:
            score += scoring["per_bridge"] if edge in bridges else 0
        score += scoring["articulation_point"] if node in artic_points else 0
    score += degree - ecc
    return score




