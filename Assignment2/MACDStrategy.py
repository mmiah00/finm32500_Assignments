

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
        # self.cash = initial_cash
    
    def run(self, price_data): 
        print ("Running MACD Strategy...")
        MACDs = {} # key = ticker, value = MACD values 
        signal_lines = {} # key = ticker, value = signal line value 

        for ticker, price_series in price_data.items(): 
            ema12s = price_series.ewm(span=12, adjust=False).mean() 
            ema26s = price_series.ewm(span=26, adjust=False).mean() 

            MACDs[ticker] = ema12s - ema26s 
            signal_line[ticker] = MACD.ewm(span=9, adjust=False).mean() 


        for i in range (len(dates)): 
            date = dates[i] 


            for ticker in MACDs: 
                if MACDs[ticker].iloc[i] > signal_lines[ticker].iloc[i]: 
                    # ema12[i] is greater than ema26[i], buy the signal 
                    price_series = price_data[ticker]
                    try:
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        # print (f"Couldn't buy 1 share of {ticker} at price {price_series.iloc[i]}. Current cash: {self.cash}. Attempted purchase amount: {price_series.iloc[i]}.")
                        pass 


            