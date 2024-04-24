import networkx as nx


# This sets the node values and edge tuple values
nodes = [1,2,3,4,5]
edges = [(1,2), (2,3), (3,4), (4,5)]


# Creates new graph and adds the nodes and edges
g = nx.Graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)


# Creates count_nodes function
def count_nodes(graph):
    return graph.number_of_nodes()  
'''
I asked ChatGPT some good methods for counting the number of nodes in a NetworkX
graph, and it said that NetworkX has a built-in function to get the number of nodes.
'''


# Calls Function and prints it
print("Node Count:", count_nodes(g)) 
