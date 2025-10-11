import pandas as pd
import numpy as np
from Strategy import Strategy

class NaiveMovingAverageStrategy(Strategy):

    def __init__ (self, initial_cash=1000000): 
        """
        Moving Average Strategy
        - Buy if 20-day MA > 50-day MA 
        
        Args:
            initial_cash: starting cash
        """
        super().__init__(initial_cash)
    
    def run(self, price_data): 
        # print ("Running Moving Average Strategy...")

        for ticker, price_series in price_data.items(): 
            ma20 = price_series.rolling(window=20).mean()
            ma50 = price_series.rolling(window=50).mean()
            buy_signals = ma20 > ma50  # boolean Series
            dates = price_series.index

            buy_dates = price_series.index[buy_signals]
            for date in buy_dates:
                try:
                    self._buy(ticker, price_series.loc[date], 1, date)
                except Exception:
                    pass
                self._record(date, price_data)