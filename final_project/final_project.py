########################################################################################
# Import required libraries
import os
import json
import requests

# Import libraries and functions from Alpaca
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
########################################################################################
# Set up Alpaca API


# Set up account info
api_key = "PKVAOU0PQU78NYSREO70"
secret_key = "NiAl6N3pDSrmS4iMudIdOmhdypHXUccsGvdIbwbG"

# Set up URLs for requests
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)

# Set headers for url requests
headers = {
    "APCA-API-KEY-ID": api_key,
    "APCA-API-SECRET-KEY": secret_key}

# Create trading client to reference when placing orders
trading_client = TradingClient(api_key, secret_key, paper=True)

# Get account info
def get_account():
    r = requests.get(ACCOUNT_URL, headers=headers)
    return json.loads(r.content)
account = get_account()

# Print account info
def PrintAccount():
    print("\n------------------------------------------------------------\n")
    for k,v in account.items():
        print(f"{k:30}{v}")
    print("\n------------------------------------------------------------\n")
PrintAccount()


########################################################################################
# Create buy, sell, and short orders. Sell and short are the same but have different names for organization

# Assign data to a variable and call the api to submit that data
def CreateBuy(symbol, price):
    
    # If account has enough buying power, then make the purchase. Display a message if not
    if float(account['buying_power']) >= price:
        
        # Set market order data
        market_order_data = MarketOrderRequest(
            symbol = symbol,
            qty = 1,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.GTC
            )
        
        # Place order
        market_order = trading_client.submit_order(
            order_data = market_order_data
            )
    else:
        print("You don't have enough money to place this order")

def CreateSell(symbol):
    
    # Set market order data
    market_order_data = MarketOrderRequest(
        symbol = symbol,
        qty = 1,
        side = OrderSide.SELL,
        time_in_force = TimeInForce.GTC
        )
    
    # Place order
    market_order = trading_client.submit_order(
        order_data = market_order_data
        )

def CreateShort(symbol):
    
    # Set market order data
    market_order_data = MarketOrderRequest(
        symbol = symbol,
        qty = 1,
        side = OrderSide.SELL,
        time_in_force = TimeInForce.GTC
        )
    
    # Place order
    market_order = trading_client.submit_order(
        order_data = market_order_data
        )


########################################################################################
# Gather stock data from the api and add it to CSVs. Save results to a json.


# Gather stock data from the api and add it to CSVs
def FetchStockData(stock):
    
    # Set up api for pulling stock data and add it to a dictionary
    alphavantage_api_key = 'GYK6HUQMJBA0DD9T'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=full&apikey={alphavantage_api_key}'
    request = requests.get(url)
    rqstDictionary = json.loads(request.text)
    
    # Set variables to pull
    key1 = "Time Series (Daily)"
    key2 = "4. close"
    
    # Set file path for saving CSVs
    file_path = f"/home/ubuntu/environment/final_project/data/{stock}.csv"
    
    # If path exists, append the data, if not, pull new data
    if os.path.exists(file_path):
        with open(file_path, "r") as csvFile:
            lines = csvFile.readlines()
        latest_date = lines[-1].split(", ")[0]
        
        newLines = []
        for date in rqstDictionary[key1].keys():
            if date == latest_date:
                break
            else:
                newLines.append(f"{date}, {rqstDictionary[key1][date][key2]}\n")
                
        newLines = newLines[::-1]  # Flip data
        
        with open(file_path, "a") as file:
            file.writelines(newLines)
    else:
        with open(file_path, "w") as file:
            for date in rqstDictionary[key1].keys():
                file.write(f"{date}, {rqstDictionary[key1][date][key2]}\n")

# Save results to a json
def SaveResults(results):
    json.dump(results, open("/home/ubuntu/environment/final_project/results.json", "w"), indent=4)


########################################################################################
# Define and create strategies


# Create and run a Mean Reversion Strategy
def MeanReversion(prices, stock):   
    
    # Initialize variables
    first_buy = 0
    buy = 0         
    sell = 0
    short = 0
    total_profit = 0
    band = 0.04
    
    # For each price, check actions such as buy, sell, or short
    for i, price in enumerate(prices):
        
        # As long as i is greater than 5 (to account for average) then check actions
        if i >= 5:
            
            # Calculate moving average
            avg = sum(prices[i-5:i]) / 5
            
            # Buy logic
            if price < avg * (1-band) and buy == 0:
                buy = price
                
                # If the first time buying, change first_buy
                if first_buy == 0:         
                    first_buy = price
                
                # Reset short logic
                if short != 0 and buy != 0:
                    total_profit += short - buy
                    short = 0
                    
            # Sell logic
            elif price > avg * (1+band) and buy != 0: 
                sell = price
                
                # Short logic
                if short == 0:
                    short = price
                total_profit += sell - buy
                
                # Reset buy
                buy = 0
                
        # At the end of the list (the most recent price) decide if we should buy, sell, or short
        # Run the same logic as the strategy, but print and call actions to buy, sell, or short the stock
        if i == len(prices) - 1:
            print(f"{stock} Mean Reversion Strategy Output:")
            if price < avg * (1-band) and buy == 0:
                print(f"You should buy this stock today at {price}!")
                CreateBuy(stock, price)
            elif price > avg * (1+band) and buy != 0:
                if short == 0:
                    print(f"You should short this stock today at {price}!")
                    CreateShort(stock)
                else:
                    print(f"You should sell this stock today at {price}!")
                    CreateSell(stock)
    
    # Calculate total profit and display it as a percentage
    total_profit = round(total_profit, 2)
    returns = f"{round(((total_profit - first_buy) / first_buy * 100), 2)}%"
    
    # Print strategy performance on stock
    print(f"Total profit: {total_profit}")
    print(f"Percent return: {returns}")
    print("---------------")
    
    # Return values to be added to results later
    return total_profit, returns

# Create and run a Simple Moving Average Strategy
def SimpleMovingAverage(prices, stock):
    
    # Initialize variables
    first_buy = 0
    buy = 0           
    sell = 0
    short = 0
    total_profit = 0
    
    # For each price, check actions such as buy, sell, or short
    for i, price in enumerate(prices): 
        
        # As long as i is greater than 5 (to account for average) then check actions
        if i >= 5:
            
            # Calculate moving average
            avg = sum(prices[i-5:i]) / 5
            
            # Buy logic
            if price > avg and buy == 0: 
                buy = price
                
                # If the first time buying, change first_buy
                if first_buy == 0:         
                    first_buy = price
                
                # Reset short logic
                if short != 0 and buy != 0:
                    total_profit += short - buy
                    short = 0
            
            # Sell logic   
            elif price < avg and buy != 0: 
                sell = price
                
                # Short logic
                if short == 0:
                    short = price
                total_profit += sell - buy
                
                # Reset buy
                buy = 0
            
        # At the end of the list (the most recent price) decide if we should buy, sell, or short
        # Run the same logic as the strategy, but print and call actions to buy, sell, or short the stock
        if i == len(prices) - 1:
            print(f"{stock} Simple Moving Average Strategy Output:")
            if price < avg and buy == 0:
                print(f"You should buy this stock today at {price}!")
                CreateBuy(stock, price)
            elif price > avg and buy != 0:
                if short == 0:
                    print(f"You should short this stock today at {price}!")
                    CreateShort(stock)
                else:
                    print(f"You should sell this stock today at {price}!")
                    CreateSell(stock)
                    
    # Calculate total profit and display it as a percentage
    total_profit = round(total_profit, 2)
    returns = f"{round(((total_profit - first_buy) / first_buy * 100), 2)}%" 
    
    # Print strategy performance on stock
    print(f"Total profit: {total_profit}")
    print(f"Percent return: {returns}")
    print("---------------")
    
    # Return values to be added to results later
    return total_profit, returns

# Create and run a Bollinger Bands Strategy
def BollingerBands(prices, stock):
    
    # Initialize variables
    first_buy = 0
    buy = 0           
    sell = 0
    short = 0
    total_profit = 0
    band = 0.04
    
    # For each price, check actions such as buy, sell, or short
    for i, price in enumerate(prices):
        
        # As long as i is greater than 5 (to account for average) then check actions
        if i >= 5:
            
            # Calculate moving average
            avg = sum(prices[i-5:i]) / 5
            
            # Buy logic
            if price > avg * (1+band) and buy == 0:  
                buy = price
                
                # If the first time buying, change first_buy
                if first_buy == 0:         
                    first_buy = price
                
                # Reset short logic
                if short != 0:
                    total_profit += short - buy
                    short = 0
                    
            # Sell logic
            elif price < avg * (1-band) and buy != 0: 
                sell = price
                
                # Short logic
                if short == 0:
                    short = price
                total_profit += sell - buy
                
                # Reset buy
                buy = 0
                
        # At the end of the list (the most recent price) decide if we should buy, sell, or short
        # Run the same logic as the strategy, but print and call actions to buy, sell, or short the stock
        if i == len(prices) - 1:
            print(f"{stock} Bollinger Bands Strategy Output:")
            if price > avg * (1+band) and buy == 0:
                print(f"You should buy this stock today at {price}!")
                CreateBuy(stock, price)
            elif price < avg * (1-band) and buy != 0:
                if short == 0:
                    print(f"You should short this stock today at {price}!")
                    CreateShort(stock)
                else:
                    print(f"You should sell this stock today at {price}!")
                    CreateSell(stock)
    
    # Calculate total profit and display it as a percentage
    total_profit = round(total_profit, 2)
    returns = f"{round(((total_profit - first_buy) / first_buy * 100), 2)}%" 
    
    # Print strategy performance on stock
    print(f"Total profit: {total_profit}")
    print(f"Percent return: {returns}")
    print("---------------")
    
    # Return values to be added to results later
    return total_profit, returns


# Define strategies
strategies = {
    "mr": {
        "id": "mr",
        "name": "Mean Reversion Strategy",
        "function": MeanReversion
    },
    "sma": {
        "id": "sma",
        "name": "Simple Moving Average Strategy",
        "function": SimpleMovingAverage
    },
    "bb": {
        "id": "bb",
        "name": "Bollinger Bands Strategy",
        "function": BollingerBands
    }
}


########################################################################################
# Initialize variables, determine stocks


# Determine stocks
stocks = ["AAPL", "ADBE", "AMZN", "GOOG", "KO", "META", "MSFT", "NVDA", "PEP", "TSLA"]

# Initialize results and stock_profits dictionaries
results = {}
stock_profits = {}

# For each stock, bring in the most recent data, add their prices to a list, then add prices to results
for stock in stocks:
    
    # Call FetchStockData function to pull in stock data for each stock
    # FetchStockData(stock)
    
    # For each line in the stock's CSV, create a list of lines
    with open(f'/home/ubuntu/environment/final_project/data/{stock}.csv', "r") as file:
        lines = file.readlines()
        
    # Create a list of prices by taking the price from each line in lines
    prices = [round(float(line.split(', ')[1]), 2) for line in lines[1:]]
    
    # Add each list of prices to the results dictionary
    results[f"{stock}_prices"] = prices
    
    
    # Run strategies and store results
    for strategy_id, strategy_info in strategies.items():
        strategy_name = strategy_info["name"]
        strategy_function = strategy_info["function"]
        
        
        # For each strategy, store the results in the results dictionary
        results[f"{stock}_{strategy_id}_profit"], results[f"{stock}_{strategy_id}_returns"] = strategy_function(prices, stock)
        
        # For each strategy, store the profits in the profits dictionary
        stock_profits[f"{stock}_{strategy_id}_profit"] = results[f"{stock}_{strategy_id}_profit"]


########################################################################################
# Determine best stock and strategy to make recommendations, then save results


# Find the best strategy and best stock by finding the highest profit in the stock_profits dictionary
best_stock_strategy = max(stock_profits, key=stock_profits.get)

# Separate stock and strategy from the best stock and strategy variable
best_stock, strategy_id, _ = best_stock_strategy.split("_")

# Get the name of the best strategy, given the id
best_strategy = strategies[strategy_id]["name"]

# Get the number which matches the best stock and strategy, then make it a currency
best_stock_number = stock_profits[best_stock_strategy]
best_stock_number = f"${best_stock_number:,.2f}"

# Print final findings
print(f"\nThe best stock is {best_stock}, using {best_strategy}, with a total profit of {best_stock_number}.")

# Finally, save the results dictionary to a json
SaveResults(results)




