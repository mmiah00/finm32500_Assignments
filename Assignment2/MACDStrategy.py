

import pandas as pd
import numpy as np
from Strategy import Strategy

class MACDStrategy(Strategy):

    def __init__ (self, initial_cash=1000000): 
        """
        MACD Strategy
        - Buy if MACD line crosses above signal line Price + momentum

        Args:
            initial_cash: starting cash
        """
        super().__init__(initial_cash)
    
    def run(self, price_data): 
        for ticker, price_series in price_data.items(): 
            ema12s = price_series.ewm(span=12, adjust=False).mean() 
            ema26s = price_series.ewm(span=26, adjust=False).mean() 
            MACD = ema12s - ema26s 



            rolling_vols = price_series.rolling(window=20).std()
            returns = price_series.pct_change()
            dates = price_series.index 

            for i in range (len(rolling_vols)): 
                if returns.iloc[i] > rolling_vols.iloc[i]: 
                    # buy ticker 
                    try:
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                    except Exception as e: 
                        print (f"Couldn't buy 1 share of {ticker} at price {price_series.iloc[i]}. Current cash: {self.cash}. Attempted purchase amount: {price_series.iloc[i]}.")

                self._record (dates[i], price_data)