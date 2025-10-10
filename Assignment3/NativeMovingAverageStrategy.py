import pandas as pd
import numpy as np
from Strategy import Strategy

class MovingAverageStrategy(Strategy):

    def __init__ (self, initial_cash=1000000): 
        """
        Moving Average Strategy
        - Buy if 20-day MA > 50-day MA 
        
        Args:
            initial_cash: starting cash
        """
        super().__init__(initial_cash)
        # self.cash = initial_cash
    
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

            # for date, signal in zip(dates, buy_signals):
            #     if signal:
            #         try:
            #             self._buy(ticker, price_series.loc[date], 1, date)
            #         except Exception as e:
            #             pass  # skip if not enough cash
            #     self._record(date, price_data)
        '''
        ma20 = {} # key = ticker, value = 20 day rolling averages (pd.Series) 
        ma50 = {} # key = ticker, value = 50 day rolling averages (pd.Series) 
        dates = None 

        for ticker, price_series in price_data.items(): 
            rolling_avgs20 = price_series.rolling(window=20).mean()
            rolling_avgs50 = price_series.rolling(window=50).mean()
            dates = price_series.index 
            ma20[ticker] = rolling_avgs20
            ma50[ticker] = rolling_avgs50
        
        for i in range (len(dates)): 
            date = dates[i] 

            for ticker in ma20: 
                if ma20[ticker].iloc[i] > ma50[ticker].iloc[i]: 
                    # buy ticker 
                    price_series = price_data[ticker]
                    try: 
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        # print (f"MA20 for {ticker} on day {dates[i]} ({rolling_avgs20.iloc[i]}) is greater than MA50 for {ticker} on day {dates[i]} ({rolling_avgs50.iloc[i]}). Buying signal.")
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        # print (f"Not enough cash to make purchase of 1 share of {ticker} on {dates[i]}. Current cash balance: {self.cash}. Attempted purchase: {price_series.iloc[i]}")
                        pass
        '''