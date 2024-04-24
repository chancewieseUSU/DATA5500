########################################################################################
# imports libraries

import requests
import json
import networkx as nx
from networkx.classes.function import path_weight
from itertools import permutations
from itertools import combinations


########################################################################################
# Sets cryptos and tickers and loads them in from the api

cryptocurrencies = {
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
    "litecoin": "ltc",
    "ethereum": "eth",
    "bitcoin": "btc"}
cryptos = list(cryptocurrencies.keys())
tickers = list(cryptocurrencies.values())

url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + ','.join(cryptos) + '&vs_currencies=' + ','.join(tickers)    # Sets URL for api pull
request = requests.get(url)   # Pulls the URL
initial_crypto_dict = json.loads(request.text)    # Uses JSON to create a dictionary of the cryptos

# initial_crypto_dict = {'bitcoin': {'xrp': 113989, 'bch': 107.728, 'eos': 67072, 'ltc': 702.546, 'eth': 19.895436, 'btc': 1.0}, 'bitcoin-cash': {'xrp': 1058, 'bch': 1.0, 'eos': 622.379, 'ltc': 6.51915, 'eth': 0.18462007, 'btc': 0.0092783}, 'cardano': {'xrp': 1.015982, 'bch': 0.00096017, 'eos': 0.59780706, 'ltc': 0.00626177, 'eth': 0.00017733, 'btc': 8.91e-06}, 'eos': {'xrp': 1.699048, 'bch': 0.00160572, 'eos': 1.0, 'ltc': 0.0104717, 'eth': 0.00029655, 'btc': 1.49e-05}, 'ethereum': {'xrp': 5728, 'bch': 5.413652, 'eos': 3371, 'ltc': 35.305118, 'eth': 1.0, 'btc': 0.05024759}, 'litecoin': {'xrp': 162.19, 'bch': 0.15328135, 'eos': 95.433, 'ltc': 1.0, 'eth': 0.028309, 'btc': 0.0014227}, 'ripple': {'xrp': 1.0, 'bch': 0.00094513, 'eos': 0.58844056, 'ltc': 0.00616366, 'eth': 0.00017455, 'btc': 8.77e-06}}
# ^^ This is a test dictionary so I don't use up my free api pulls
# Pulling from https://api.coingecko.com/api/v3/simple/price?ids=ripple,cardano,bitcoin-cash,eos,litecoin,ethereum,bitcoin&vs_currencies=xrp,ada,bch,eos,ltc,eth,btc

crypto_dict = {}    # Initializes new crypto dictionary
for old_key, value in initial_crypto_dict.items():  # This changes the keys from full names to abbreviations (bitcoin --> btc)
    new_key = cryptocurrencies[old_key]     # Sets the new key to the abbreviation of the full name, found in my cryptocurrencies dictionary
    crypto_dict[new_key] = value        # Adds to new dictionary so it will be easier to loop through tickers/nodes
    
########################################################################################
# Create a graph and adds edges

g = nx.DiGraph() # Creates graph
edges = []  # Creates new blank list of edges
for ticker1, ticker2 in permutations(tickers,2):    # Iterates through each possible case of edges, both ways
    try:
        rate = crypto_dict[ticker1][ticker2]    # Sets the exchange rate given the two tickers
    except KeyError:
        continue                            # continues if there is a KeyError
    edges.append((ticker1,ticker2,rate))    # Adds edges to the list of edges

g.add_weighted_edges_from(edges)        # Adds weighted edges, given the edges and rates

path_weights = {}           # Initializes the path weights
path_weights_reverse = {}   # Initializes the reverse path weights

########################################################################################
# Calculate the weight (currency exchange rate) of every path

for t1, t2 in combinations(g.nodes, 2):     # Given two tickers, checks all combinations, without duplicates. (Later will reverse to go first to second) (Originally had tickers here instead of nodes but I wanted to show my nodes are working)
    print("All paths between", t1, "and", t2, "-----------------------------\n")
    if nx.has_path(g,t1,t2) == False:    # Checks to make sure there is a path. If not, it prints to inform there is no path
        print("There are no paths between",t1, "and", t2, "\n")
    for path in nx.all_simple_paths(g, t1, t2): # Iterates through each path 
        path_weight_to = 1.0            # Sets a default path weight to 1as we'll be multiplying
        for i in range(len(path) - 1):                      # For every path, calculates the weight of each exchange rate
            path_weight_to *= g[path[i]][path[i+1]]['weight']
        print("Path to:", path,"---- Path weight: ", path_weight_to)
        
        path.reverse()                      # Reverses the path to check from the second to the first ticker this time
        path_weight_from = 1.0     # Sets initial path weight to 1
        for i in range(len(path) - 1):                      # For every path, calculates the weight of each exchange rate
            path_weight_from *= g[path[i]][path[i+1]]['weight']
        print("Path from:", path,"---- Path weight: ", path_weight_from)
        path_weight = path_weight_to * path_weight_from     # Calculates the total weight of the path
        print("Total path weight:", path_weight, "\n")
        # input()   # Used this for testing
        
        path_weights_reverse[str(path)] = path_weight   # Adds to dictionary of the reverse paths so I can print that later
        path.reverse()                                  # Reverses path back to original form
        path_weights[str(path)] = path_weight           # Adds to dictionary of the original paths so I can print that later
        
    print("-----------------------------------------------------\n")


########################################################################################
# Calculate the best and worst weights

# Calulates and prints greatest weight factor & path
best_path = max(path_weights, key=lambda k: path_weights[k])
best_path_reverse = max(path_weights_reverse, key=lambda k: path_weights_reverse[k])
best_value = path_weights[best_path]
print("Greatest Paths weight factor:", best_value)
print("Paths", best_path, best_path_reverse, "\n")

# Calulates and prints smallest weight factor & path
worst_path = min(path_weights, key=lambda k: path_weights[k])
worst_path_reverse = min(path_weights_reverse, key=lambda k: path_weights_reverse[k])
worst_value = path_weights[worst_path]
print("Smallest Paths weight factor:", worst_value)
print("Paths", worst_path, worst_path_reverse)


########################################################################################
# Save graph as an image for review

import matplotlib       # Import matplot to create visual
matplotlib.use('Agg')   # Sets visual to server-only mode, with no GUI
import matplotlib.pyplot as plt 
import os
curr_dir = os.path.dirname(__file__)        # Sets current directory to put visual in same place as code
graph_visual_fil = curr_dir + "/" + "graph_visual.png"  # Create file for visual
pos=nx.circular_layout(g)               # Code here and below sets perameters for the visual and assins it to the file
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.savefig(graph_visual_fil)