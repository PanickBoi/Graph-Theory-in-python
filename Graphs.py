import networkx as nx
import matplotlib.pyplot as plt
import random


save_file = False #determinesi f the result should be stored in a file
graph_info = False #prints info for each node in the graph

    
premade = True #If true allows V & E to be set directly
simple_graph = False #if true only lets a simple graph to be created

#Node Generation Limiters
limit_connections = True #Self-explanatory
con_dec = True # Exponentially decreases the connection chance when adding a connection to the node
min_con = 1 #Ensures nodes have at least n connections (must be lower than con_limit)
con_limit = 8 #Connection Limit of each node




gct = {} #// Global Connection Table
gdt = {} #// Global Degree Table

#def dfs_importance(node):
    #score = 0
def general_graph():
    nodes = int(input("Give amount of nodes: "))
    while type(nodes) != type(5): #input handling
        nodes = int(input("Error,Give amount of nodes: "))
    con_chance = float(input("Give connection chance: "))
    while type(con_chance) != type(5.0):#input handling
        con_chance = float(input("Error,Give connection chance: "))
    return (nodes,con_chance)

def most_important_node(nodes): # A simple algorithm i thought
    #Takes the Node list and:
    #-parses through nodes one-by-one
    #-Calculates for each node the sum of all it's neighbor degrees
    #-returns the best node,which is the one with the biggest sum
    
    best = 0
    bestNode = 0
    for node in nodes:
        score = 0
        for neighbor in gct[node]:
            score += gdt[neighbor]
        if score > best:
            best = score
            bestNode = node
    print(bestNode,"With importance of:",best)
    

while True: #QoL
    
    G =  None #Empty..
    V = [] #V is the set of vertices/nodes of G
    E = [] #E is the set of edges/connections of G
 
    #// Pre-made demo,change as you wish
    gV = [1,2,3,4,5,6,7,8]
    gE = [[1,3],[1,4],[1,5],[2,3],[2,5],[2,8],[3,4],[3,8],[7,8]]
    
    if not premade:
        gct = {}
        gg = general_graph()
        nodes,con_chance = gg[0],gg[1]
            
        for node in range(nodes):
            V.append(node)
            gct[node] = [] #initializes the key-value per in GCT
        for i in range(len(V)):
            con = len(gct[i])
            for j in range(len(V)):
                if V[i] == V[j]: #Makes sure the node isnt targeting itself
                    continue
                r = random.random()*100
                if con_dec:
                    r*=con+1 #Simple exponential decrease function
                #print(i,con,r)
                if  r <= con_chance or min_con > con: #checks if the random chance passes (or if the node requires a connection if min_con >0)
                    if not limit_connections or (limit_connections and con < con_limit) and (len(gct[i]) < con_limit and len(gct[j]) < con_limit):
                        #Checks if the node is limited in the amount of connections, and if do,check for room for one more connection
                        #then checks the targeting node if it room for 1 more connection too
                        gct[i].append(V[j])
                        gct[j].append(V[i])
                        E.append([V[i],V[j]])
                        con+=1
                gdt[i] = len(gct[i]) #Initializes the GDT which is uses for the most_importnat_node function
    else:
        if simple_graph:
            V = gV
            E = gE
            G = nx.Graph()
            G.add_nodes_from(V)
            G.add_edges_from(E)
        else:
            #change the code to display whatever relationship between data you want.
            #below is the implementation of a friendship graph
            G = nx.DiGraph()
            #User input settings
            print("// Choose Input mode //\n-Manual (M)\n-General (G)\n-Insert File(I)")
            mode = input("Choose Mode:").upper()
            while mode not in "MGI":
                mode = input("Choose a correct Mode:")
            if mode == "G":
                gg = general_graph()
                nodes,con_chance = gg[0],gg[1]
                G.add_nodes_from(list(range(nodes)))
                
                for node_i in G.nodes(): #This only makes a node connect to another node
                    for node_j in G.nodes(): #not the other way around
                        if node_i != node_j:
                            r = random.random()*100
                            con = len(list(G.successors(node_i)))
                            if con_dec:
                                r*=con+1 #Simple exponential decrease function
                            a = limit_connections and con < con_limit 
                            b = not a and con < con_limit 
                            if (a or b) and r <= con_chance: #i am not explaining this
                                G.add_edge(node_i,node_j) 
                        else:
                            continue
                for node in G.nodes():
                    size = len(list(G.predecessors(node)))+.5
                    color = len(list(G.successors(node)))
                    #The higher the number of outgoing connections,the redder the node
                    #The bigger of incoming connections,the bigger the node
                    r,g,b = 0,0,0
                    
                    r = min(int((color / con_limit)*255),255)
                    b = min(int((size / con_limit)*255) ,255)
                        
                    c = (r/255, g/255, b/255)

                    G.nodes[node].update({'color': c,'size':size}) 
            elif mode == "M":
                nodes = int(input("Give amount of nodes: "))
                while type(nodes) != type(5): #input handling
                    nodes = int(input("Error,Give amount of nodes: "))
                G.add_nodes_from(list(range(nodes)))
                
                for node in range(nodes): #by-hand, edge painting
                    print("Provide Connections in the following format: 1423   <- This are the Nodes the CURRENT node POINTS towards to (No Spaces)")
                    cons = input("Node "+str(node)+" ,Provide Connections: ")
                    while type(cons) != type(""): #input handling
                        cons = input("Node "+str(node)+" ,Error,Provide Connections: ")
                    for con in cons:
                        G.add_edge(node,int(con))
                for node in G.nodes():
                    size = len(list(G.predecessors(node)))+.5
                    color = len(list(G.successors(node)))
                    #The higher the number of outgoing connections,the redder the node
                    #The bigger of incoming connections,the bigger the node
                    r,g,b = 0,0,0
                    
                    r = min(int((color / nodes)*255),255)
                    b = min(int((size / nodes)*255) ,255)
                        
                    c = (r/255, g/255, b/255)

                    G.nodes[node].update({'color': c,'size':size})
            elif mode == "I":
                print("Note: \n\nFiles must be in the format of:\nN C\nWhere N->The name/number of the node,followed by a whitespace\nandC-> The connections this node has,MUST be seperated by a COMMA ','")
                file_name = input("Give file name (Must be in the same directory as this script):")
                V = []
                E = []
                is_simple = input("Does the file contain a simple graph? (Otherwise it's interpretated as a directional graph)(Y/N):")
                if is_simple:
                    G = nx.Graph()
                while is_simple.upper() not in "YN":
                    is_simple = input("Error,Does the file contain a simple graph? (Otherwise it's interpretated as a directional graph)(Y/n):")
                with open(file_name, "r") as f:
                        for node_info in f:
                            sl = node_info.split()
                            node = sl[0]
                            cons = sl[1].split(",")
                            V.append(node)
                            for con_node in cons:
                                if is_simple == "Y":
                                    if [con_node, node] not in E:
                                        E.append([node, con_node])
                                else:
                                    E.append([node, con_node])
                   
                G.add_nodes_from(V)
                G.add_edges_from(E)
                for node in G.nodes():
                    size = G.neighbors(node)
                    color = G.degree(node)
                    if not is_simple:
                        size = len(list(G.predecessors(node)))+.5
                        color = len(list(G.successors(node)))
                    #The higher the number of outgoing connections,the redder the node
                     #The bigger of incoming connections,the bigger the node
                    r,g,b = 0,0,0
                    
                    r = min(int((color / con_limit)*255),255)
                    b = min(int((size / con_limit)*255) ,255)
                        
                    c = (r/255, g/255, b/255)

                    G.nodes[node].update({'color': c,'size':size})
    if graph_info:
        print("G has order |V(G)|=",G.order(),"and size |E(G)|=",G.size())
        print("V(G):",G.nodes()) #print the nodes of G
        print("E(G):", G.edges()) #print the edges of G
        for v in G:
            print("The neighbors of", v, "are:", list(G.neighbors(v)))
    #// Display        
    node_colors = [G.nodes[n].get('color', (0.5, 0.5, 0.5)) for n in G.nodes()] #extract color per node
    node_sizes  = [G.nodes[n].get('size', 300) * 100 for n in G.nodes()] #same but for size   
    avg_size = sum(node_sizes) / max(len(node_sizes), 1) #avg size
    k = (avg_size / 300) * (1 / max(G.order() ** 0.5, 1)) #Scale spacing by avg size and node count
    pos = nx.spring_layout(G, k=k, seed=67)#layout with dynamic spacing
    nx.draw_networkx(G, pos=pos, node_color=node_colors, node_size=node_sizes) #draw the graph
    #//
    
    #nx.draw_networkx(G) #Draw the graph G
    if save_file:
        plt.savefig("lect01a.eps") #Save the drawing of G
    #most_important_node(V)
    print("Degree List:\nNode | Degree")
    for node,degree in gdt.items():
        print(node," | ",degree)
    plt.show() #Show the drawing of G on screen
