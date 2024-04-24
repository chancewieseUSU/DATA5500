import networkx as nx
import random

# This sets the node values
nodes = [1,2,3,4,5,6,7,8,9,10]


#creates 50 random edges
edges = []
for i in range(50):     
    node1 = random.choice(nodes)    # I asked ChatGPT a good way to pull a random item from my list I made.
    node2 = random.choice(nodes)    # Sets both parts of the tuple
    edge_tuple = (node1, node2)     # Creates tuple
    edges.append(edge_tuple)        # Adds tuple to list of tuples


# Creates new graph and adds the nodes and edges
g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)


# Creates count_nodes_degree_greater_than_5 function
def count_nodes_degree_greater_than_5(graph):
    node_count = 0                      #Sets node counter
    for node in graph.nodes():          #iterates through the nodes in the graph
        if graph.degree[node] > 5:      #Checks if degree is more than 5 and adds it to a counter
            node_count += 1
    return node_count                   #returns node count for function
'''
I asked ChatGPT how to find the degree of nodes within a NetworkX graph. 
It gave me graph.degree[node], which is a function of NetworkX.
'''


# Prints nodes and edges to check work
print("Nodes:", nodes)
print("Edges:", edges, "\n")


# Calls Function and prints it
print("Node Count:", count_nodes_degree_greater_than_5(g)) 

