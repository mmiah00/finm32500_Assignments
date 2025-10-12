# '''
# WindowedMovingAverageStrategy: Maintain a fixed-size buffer and update the average incrementally (Time: O(1), Space:
# O(k), where k is window size). 
# '''

from collections import deque
from collections import defaultdict
buffer = deque(maxlen=k)

class WindowedMovingAverageStrategy (Strategy): 
    def __init__ (self, initial_cash=1000000, window_size = 20): 
        super().__init__(initial_cash)
        self.window_size = window_size 
    
    def run(self, data): 
        # data is a dict where key = ticker, value = list of MDPs for that ticker  
        signals = defaultdict (list) # key = ticker, value = list of tickers (i.e. ["BUY", "HOLD", "HOLD", "SELL", etc])
        
        for ticker in data: 
            mdps = data[ticker]
            buffer = deque(maxlen=self.window_size) # space: O(K), where K is the window size 

            prev_avg = 0 

            for mdp in mdps: 
                n = min(len(buffer) + 1, self.window_size)
                price = mdp.price 

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
    
    