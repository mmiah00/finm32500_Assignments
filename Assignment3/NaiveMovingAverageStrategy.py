import pandas as pd
import numpy as np
from Strategy import Strategy

class NaiveMovingAverageStrategy(Strategy):

    def __init__ (self, window_size=20): 
        self.window_size = window_size 
        self.prices = []
    
    def generate_signals(self, mdps): 
        signals = [] 

        for mdp in mdps: 
            if len(prices) < self.window_size: 
                self.prices.append(mdp.price)
                signals.append('HOLD')
            else: 
                avg = np.mean(signals[-self.window_size:]) # last k elements, which is the size of the window 
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