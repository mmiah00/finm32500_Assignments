import pandas as pd
import numpy as np
from Strategy import Strategy

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
                    signals.append('HOLD')
                else: 
                    avg = np.mean(prices[-self.window_size:]) # last k elements, which is the size of the window 
                    if mdp.price > avg: 
                        signals.append('BUY')
                    elif mdp.price < avg: 
                        signals.append('SELL')
                    else: 
                        signals.append('HOLD')
                
        return signals 

        # Time Complexity: O(N) -> This algorithm calculates the moving average for each market data point 
        #                          in the data, so as the number of data points increases, the time it takes 
        #                          to the run the algorithm increases as well as there are more data points 
        #                          to process.  

        # Space Complexity: O(N) -> This algorithm stores the moving averages for each data point in an array, 
        #                           which takes up O(N) space.  

# from data_loader import MDPs

# strat = NaiveMovingAverageStrategy() 
# print(strat.generate_signals(MDPs))