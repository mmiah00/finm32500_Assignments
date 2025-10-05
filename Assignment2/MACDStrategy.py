

import pandas as pd
import numpy as np
from Strategy import Strategy

class MACDStrategy(Strategy):

    def __init__ (self, initial_cash=1000000): 
        """
        MACD Strategy
        - Buy if MACD line crosses above signal line 

        Args:
            initial_cash: starting cash
        """
        super().__init__(initial_cash)
    
    def run(self, price_data): 
        for ticker, price_series in price_data.items(): 
            ema12s = price_series.ewm(span=12, adjust=False).mean() 
            ema26s = price_series.ewm(span=26, adjust=False).mean() 

            MACD = ema12s - ema26s 
            signal_line = MACD.ewm(span=9, adjust=False).mean() 


            for i in range (len(MACD)): 
                if MACD.iloc[i] > signal_line.iloc[i]: 
                    # ema12[i] is greater than ema26[i], buy the signal 
                    try:
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        print (f"Couldn't buy 1 share of {ticker} at price {price_series.iloc[i]}. Current cash: {self.cash}. Attempted purchase amount: {price_series.iloc[i]}.")