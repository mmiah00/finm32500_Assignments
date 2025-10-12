# '''
# WindowedMovingAverageStrategy: Maintain a fixed-size buffer and update the average incrementally (Time: O(1), Space:
# O(k), where k is window size). 
# '''

from collections import deque
from collections import defaultdict
from Strategy import Strategy


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
    

# TESTING
# from data_loader import MDPs_by_ticker

# strat = WindowedMovingAverageStrategy() 
# print(strat.generate_signals(MDPs_by_ticker))