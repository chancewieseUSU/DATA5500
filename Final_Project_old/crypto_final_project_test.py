########################################################################################
# imports libraries

import requests
import json
import networkx as nx
from networkx.classes.function import path_weight
from itertools import permutations
from itertools import combinations


########################################################################################
# Set up Alpaca Trading Client
from alpaca.trading.client import TradingClient


api_key = "PKSL2HIC18LLFDQBYVSD"
secret_key = "zmhvJ2ejyIFbdsIRH3OzJRPVpjSyyl8oe7Cfoy8x"
trading_client = TradingClient(api_key,secret_key)
account = dict(trading_client.get_account())
# for k,v in account.items():
#     print(f"{k:30}{v}")
# print("\n------------------------------------------------------------\n")

########################################################################################
# Set up a list of cryptos

cryptos_url = "https://paper-api.alpaca.markets/v2/assets?asset_class=crypto&attributes="
headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKSL2HIC18LLFDQBYVSD",
    "APCA-API-SECRET-KEY": "zmhvJ2ejyIFbdsIRH3OzJRPVpjSyyl8oe7Cfoy8x"}
cryptos_request = requests.get(cryptos_url, headers=headers)

alpaca_cryptos = {}
for crypto in cryptos_request.json():
    symbol = crypto["symbol"]
    alpaca_cryptos[symbol] = crypto
cryptos = list(alpaca_cryptos.keys())

# for k,v in crypto_dict.items():
#     print(k,"\n",v,"\n")
# # print(cryptos)
# print(','.join(cryptos))

########################################################################################
# List of recent trades

trades_url = "https://data.alpaca.markets/v1beta3/crypto/us/latest/trades?symbols=" + (",".join(cryptos)).replace("/", "%2F")

headers = {"accept": "application/json"}

trades_request = requests.get(trades_url, headers=headers)
initial_trades = json.loads(trades_request.text)
trades = {}
for key, value in initial_trades['trades'].items():
    trades[key] = value
# print(trades)
for k,v in trades.items():
    print(k,"\n",v,"\n")


print("\n\n------------------------------------------------------------\n\n")


crypto_dict = {}
for key, value in trades.items():
    tokens = key.split('/')
    if len(tokens) == 2:  # Ensure the key format is as expected
        base_currency = tokens[0]
        quote_currency = tokens[1]
        if base_currency not in crypto_dict:
            crypto_dict[base_currency] = {}
        if quote_currency not in crypto_dict:
            crypto_dict[quote_currency] = {}
        crypto_dict[base_currency][quote_currency] = value['p']
        crypto_dict[quote_currency][base_currency] = 1/value['p']
# tickers = list(crypto_dict.keys())
tickers = ['UNI', 'USDC', 'BCH', 'BTC', 'USD', 'ETH', 'LTC']

# for k,v in paths.items():
#     print(k,"\n",v,"\n")
# print(paths)

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