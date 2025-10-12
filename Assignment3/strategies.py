import pandas as pd
import numpy as np
from collections import defaultdict
from collections import deque
from Strategy import Strategy

'''
NaiveMovingAverageStrategy: For each tick, recompute the average price from scratch (Time: O(n), Space: O(n)).
'''

class NaiveMovingAverageStrategy(Strategy):

    def __init__ (self, window_size=20): 
        self.window_size = window_size 
    
    def generate_signals(self, data): 
        # data is a dict where key = ticker, value = list of MDPs for that ticker 
        
        signals = defaultdict (list) # key = ticker, value = list of tickers (i.e. ["BUY", "HOLD", "HOLD", "SELL", etc])
        
        for ticker in data: 
            mdps = data[ticker]
            prices = [] 
        
            for mdp in mdps: 
                prices.append(mdp.price)
                if len(prices) < self.window_size: 
                    signals[ticker].append('HOLD')
                else: 
                    avg = np.mean(prices[-self.window_size:]) # last k elements, which is the size of the window 
                    if mdp.price > avg: 
                        signals[ticker].append('BUY')
                    elif mdp.price < avg: 
                        signals[ticker].append('SELL')
                    else: 
                        signals[ticker].append('HOLD')
                
        return signals 

        # Time Complexity: O(N) -> This algorithm calculates the moving average for each market data point 
        #                          in the data, so as the number of data points increases, the time it takes 
        #                          to the run the algorithm increases as well as there are more data points 
        #                          to process.  

        # Space Complexity: O(N) -> This algorithm stores the moving averages for each data point in an array, 
        #                           which takes up O(N) space.  




'''
WindowedMovingAverageStrategy: Maintain a fixed-size buffer and update the average incrementally (Time: O(1), Space:
O(k), where k is window size). 
'''

class WindowedMovingAverageStrategy (Strategy): 
    def __init__ (self, window_size = 20): 
        self.window_size = window_size 
    
    def generate_signals(self, data): 
        # data is a dict where key = ticker, value = list of MDPs for that ticker  
        signals = defaultdict (list) # key = ticker, value = list of tickers (i.e. ["BUY", "HOLD", "HOLD", "SELL", etc])
        
        for ticker in data: 
            mdps = data[ticker]
            buffer = deque(maxlen=self.window_size) # space: O(K), where K is the window size 

            prev_avg = 0 

            for mdp in mdps: 
                n = min(len(buffer) + 1, self.window_size)
                price = mdp.price 

                if len(buffer) < 1: 
                    buffer.append(price)
                    prev_avg = price
                    signals[ticker].append("HOLD")

                else: 
                    avg = ((prev_avg * n - buffer[0]) + price) / n
                    buffer.append(price) 

                    if price > avg: 
                        signals[ticker].append("BUY")
                    elif price < avg: 
                        signals[ticker].append("HOLD")
                    else: 
                        signals[ticker].append("SELL")

                    prev_avg = avg
        
        return signals 

        # Time Complexity: O(m*n) -> This algorithm goes through the market data points (MDPs) of each ticker and 
        #                            find the moving average in O(1) using the formula: 
        #                            avg = ((prev_avg * n - buffer[0]) + price) / n. 
        #                            The outer loop os O(m), where m is the number of tickers in our data. The 
        #                            inner loop is O(n), where n is the length of the MDPs for a given ticker (more 
        #                            specifically, the largest list of MDPs). Therefore, the overall time complexity 
        #                            of this algorithm is O(m*n). 

        # Space Complexity: O(m + k) -> This algorithm stores the signals in a dictionary for each ticker. The 
        #                               space complexity of the signals dictionary is O(m), where m is the number 
        #                               of tickers we have in our data. We store the prices in a buffer, implemented 
        #                               as a deque. The deque has size k, which is the window size of our strategy. So, 
        #                               the overall space complexity of this algorithm is O(m+k), or the larger of 
        #                               either m or k. 
    



# NAIVE MA TESTING
# from data_loader import MDPs_by_ticker

# strat = NaiveMovingAverageStrategy() 
# print(strat.generate_signals(MDPs_by_ticker))

# WINDOWED MA TESTING
# from data_loader import MDPs_by_ticker

# strat = WindowedMovingAverageStrategy() 
# print(strat.generate_signals(MDPs_by_ticker))