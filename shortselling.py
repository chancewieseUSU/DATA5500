# def BollingerBands(prices):
#     first_buy = 0
#     buy = 0           #initial values
#     sell = 0
#     profit = 0
#     total_profit = 0
#     for i in range(len(prices)):   
#         avg = (prices[i-5]+prices[i-4]+prices[i-3]+prices[i-2]+prices[i-1])/5
#         if prices[i] > avg * 1.05 and buy == 0:   
#             if first_buy == 0:         
#                 first_buy = prices[i]
#                 buy = prices[i]
#             else:
#                 buy = prices[i]
#             # print("buying at", buy)    
#         elif prices[i] < avg * 0.95 and buy != 0: 
#             sell = prices[i]
#             profit = round(sell-buy, 2)
#             total_profit += profit         
#             total_profit = round(total_profit, 2)
#             buy = 0                    
#             # print("selling at", sell)       
#             # print("trade profit:", profit)
#         else:
#             pass
#         if i == len(prices)-1 and prices[i] > avg * 1.05 and buy > 0:
#             print("You should buy this stock today!")
#         elif i ==len(prices)-1 and prices[i] < avg and buy == 0:
#             print("You should sell this stock today!")
#         else:
#             pass
        
#     returns = str(round((total_profit/first_buy*100),2))+"%" 
#     print("Total profit:", total_profit)
#     # print("First buy:", first_buy)
#     print("Percent return:", returns)
#     print("---------------")
#     return total_profit, returns
    
    
#     profit = price - buy
    
    '''
    keep track of 
    '''
    
    
    
    short = 0
    buy = 0
    sell = 0
    i = 0
    band = 0.02
    
    for price in prices:
        if i > 5:
            avg = (prices[i-1]+prices[i-2]+prices[i-3]+prices[i-4]+prices[i-5])/5
            
            # buy signal
            if price > avg * (1+ band) and buy == 0:
                print("buying at: ", price)
                buy = price
                if short != 0.0 and buy != 0.0:
                    profit += short-buy
                short = 0
            elif price < avg * (1 - band) and buy != 0:
                short = price
                print("selling at: ", price)
                
                profit += price - buy
                buy = 0
            else:
                pass