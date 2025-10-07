

import pandas as pd
import numpy as np
from Strategy import Strategy

class RSIStrategy(Strategy):

    def __init__ (self, initial_cash=1000000, period_length=14): 
        """
        RSI Strategy
        - Buy if RSI < 30

        Args:
            initial_cash: starting cash
            period_length: length of the period we are calculating RSI over 
        """
        super().__init__(initial_cash)
        self.period_length = period_length
        # self.cash = initial_cash
    
    def run(self, price_data): 

        # print ("Running RSI Strategy...")

        RSIs = {} # key = ticker, value = RSI value for each ticker 
        dates = None 

        for ticker, price_series in price_data.items(): 
            deltas = price_series.diff(1) 
            dates = price_series.index 
            gains = [0 if deltas.iloc[i] < 0 else deltas.iloc[i] for i in range (len(deltas))]
            losses = [0 if deltas.iloc[i] > 0 else deltas.iloc[i] for i in range (len(deltas))]
            
            gains = pd.Series(gains) 
            losses = pd.Series(losses) 

            avg_gains = gains.rolling(window=self.period_length).mean() 
            avg_losses = losses.rolling(window=self.period_length).mean()

            rs = avg_gains / avg_losses 

            rsi = 100 - (100 / (1 + rs))

            RSIs[ticker] = rsi 

        for i in range (len(dates)): 
            date = dates[i] 

            for ticker in RSIs: 
                if RSIs[ticker].iloc[i] < 30: 
                    #buy signal 
                    price_series = price_data[ticker]

                    try:
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        # print (f"Couldn't buy 1 share of {ticker} at price {price_series.iloc[i]}. Current cash: {self.cash}. Attempted purchase amount: {price_series.iloc[i]}.")
                        pass 






        for ticker, price_series in price_data.items(): 
            deltas = price_series.diff(1) 
            gains = [0 if deltas.iloc[i] < 0 else deltas.iloc[i] for i in range (len(deltas))]
            losses = [0 if deltas.iloc[i] > 0 else deltas.iloc[i] for i in range (len(deltas))]
            
            gains = pd.Series(gains) 
            losses = pd.Series(losses) 

            avg_gains = gains.rolling(window=self.period_length).mean() 
            avg_losses = losses.rolling(window=self.period_length).mean()

            rs = avg_gains / avg_losses 

            rsi = 100 - (100 / (1 + rs))

            for i in range(len(rsi)): 
                if rsi.iloc[i] < 30: 
                    #buy signal 
                    try:
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        print (f"Couldn't buy 1 share of {ticker} at price {price_series.iloc[i]}. Current cash: {self.cash}. Attempted purchase amount: {price_series.iloc[i]}.")