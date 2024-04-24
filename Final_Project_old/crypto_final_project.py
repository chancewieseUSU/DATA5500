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

trading_client = TradingClient("PKEZEQVBLHW7O9S1VDD7","gjHAA8Awz6wS0LT89X12NnoG8evWQtfvVJaBAmrG")
print(trading_client.get_account().account_number)
print(trading_client.get_account().buying_power)

########################################################################################
# Sets cryptos and tickers and loads them in from the api

cryptocurrencies = {
    "ripple": "xrp",
    "cardano": "ada",
    "bitcoin-cash": "bch",
    "eos": "eos",
    "litecoin": "ltc",
    "ethereum": "eth",
    "bitcoin": "btc",
    "tether": "usdt",
    "binancecoin": "bnb",
    "solana": "sol",
    "dogecoin": "doge",
    "shiba-inu": "shib",
    "cronos": "cro"
}
cryptos = list(cryptocurrencies.keys())
tickers = list(cryptocurrencies.values())

url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + ','.join(cryptos) + '&vs_currencies=' + ','.join(tickers)    
request = requests.get(url) 
initial_crypto_dict = json.loads(request.text)   

alpaca_url = 'https://paper-api.alpaca.markets'






# initial_crypto_dict = {'bitcoin': {'xrp': 113989, 'bch': 107.728, 'eos': 67072, 'ltc': 702.546, 'eth': 19.895436, 'btc': 1.0}, 'bitcoin-cash': {'xrp': 1058, 'bch': 1.0, 'eos': 622.379, 'ltc': 6.51915, 'eth': 0.18462007, 'btc': 0.0092783}, 'cardano': {'xrp': 1.015982, 'bch': 0.00096017, 'eos': 0.59780706, 'ltc': 0.00626177, 'eth': 0.00017733, 'btc': 8.91e-06}, 'eos': {'xrp': 1.699048, 'bch': 0.00160572, 'eos': 1.0, 'ltc': 0.0104717, 'eth': 0.00029655, 'btc': 1.49e-05}, 'ethereum': {'xrp': 5728, 'bch': 5.413652, 'eos': 3371, 'ltc': 35.305118, 'eth': 1.0, 'btc': 0.05024759}, 'litecoin': {'xrp': 162.19, 'bch': 0.15328135, 'eos': 95.433, 'ltc': 1.0, 'eth': 0.028309, 'btc': 0.0014227}, 'ripple': {'xrp': 1.0, 'bch': 0.00094513, 'eos': 0.58844056, 'ltc': 0.00616366, 'eth': 0.00017455, 'btc': 8.77e-06}}
# Pulling from https://api.coingecko.com/api/v3/simple/price?ids=ripple,cardano,bitcoin-cash,eos,litecoin,ethereum,bitcoin&vs_currencies=xrp,ada,bch,eos,ltc,eth,btc

crypto_dict = {}   
for old_key, value in initial_crypto_dict.items():  
    new_key = cryptocurrencies[old_key]     
    crypto_dict[new_key] = value        
    
########################################################################################
# Create a graph and adds edges

g = nx.DiGraph() 
edges = []  
for ticker1, ticker2 in permutations(tickers,2):  
    try:
        rate = crypto_dict[ticker1][ticker2]   
    except KeyError:
        continue   
    edges.append((ticker1,ticker2,rate))    

g.add_weighted_edges_from(edges)        

path_weights = {}           
path_weights_reverse = {} 

########################################################################################
# Calculate the weight (currency exchange rate) of every path

for t1, t2 in combinations(g.nodes, 2):    
    print("All paths between", t1, "and", t2, "-----------------------------\n")
    if nx.has_path(g,t1,t2) == False:    
        print("There are no paths between",t1, "and", t2, "\n")
    for path in nx.all_simple_paths(g, t1, t2):
        path_weight_to = 1.0            
        for i in range(len(path) - 1):  
            path_weight_to *= g[path[i]][path[i+1]]['weight']
        print("Path to:", path,"---- Path weight: ", path_weight_to)
        
        path.reverse()                  
        path_weight_from = 1.0     
        for i in range(len(path) - 1):
            path_weight_from *= g[path[i]][path[i+1]]['weight']
        print("Path from:", path,"---- Path weight: ", path_weight_from)
        path_weight = path_weight_to * path_weight_from    
        print("Total path weight:", path_weight, "\n")
        
        path_weights_reverse[str(path)] = path_weight 
        path.reverse()                                
        path_weights[str(path)] = path_weight         
        
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