'''
WindowedMovingAverageStrategy: Maintain a fixed-size buffer and update the average incrementally (Time: O(1), Space:
O(k), where k is window size). 
'''
from collections import deque
buffer = deque(maxlen=k)

class WindowedMovingAverageStrategy (Strategy): 
    def __init__ (self, initial_cash=1000000, window_size = 20): 
        super().__init__(initial_cash)
        self.window_size = window_size 
    
    def run(self, mdps): 
        buffer = deque(maxlen=self.window_size) # space: O(K), where K is the window size 
        signals = [] # space: O(N), where N is the number of days we are generating signals for  

        prev_avg = 0 

        for mdp in mdps: 
            n = min(len(buffer) + 1, self.window_size)
            price = mdp.price 

            avg = ((prev_avg * n - buffer[0]) + price) / n
            buffer.append(price) 

            if price > avg: 
                signals.append("BUY")
            elif price < avg: 
                signals.append("HOLD")
            else: 
                signals.append("SELL")

            prev_avg = avg 
        
        return signals 
    
    