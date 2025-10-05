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
    
    def run(self, price_data): 
        MA20 = {} # key = date, value = 20-day moving average value 
        MA50 = {} # key = date, value = 50-day moving average value 

        dates = None 

        for ticker, price_series in price_data.items(): 
            if type(dates) != pd.Series: 
                dates = price_series.index #price_series['Date']
            
            MA20 = {} # key = date, value = 20-day moving average value 
            MA50 = {} # key = date, value = 50-day moving average value 

            curr_sum1 = 0 # keeping track of average for 20 day MA
            curr_sum2 = 0 # keeping track of average for 50 day MA 

            for i in range(len(dates)): 
                day = i + 1 
                date = dates[i]

                if day < 20: 
                    curr_sum1 += prices_series[dates[i]]
                    curr_sum2 += prices_series[dates[i]]

                elif day == 20: 
                    curr_sum1 += prices_series[dates[i]]
                    avg = curr_sum1 / 20 
                    MA20[date] = avg 

                elif day >= 20 and day < 50: 
                    # cant find ma50 for days 20-50, only ma20 
                    # subtract price at day (day - 20) and find the average
                    # update MA20 dict 
                    curr_sum1 -= prices_series[dates[i - 20]]
                    curr_sum1 += prices_series[dates[i]]
                    avg = curr_sum1 / 20 

                    MA20[date] = avg 

                else: 
                    # can find ma50 for days >50
                    # subtract price at day (day - 20) to find ma20 
                    # subtract price at day (day - 50) to find ma50 
                    # find average of each 
                    # update MA20 and MA50 
                    # compare the prices and trade is MA20 > MA50 
                    curr_sum1 -= prices_series[dates[i - 20]]
                    curr_sum1 += prices_series[dates[i]]
                    avg1 = curr_sum1 / 20 

                    MA20[date] = avg1 

                    curr_sum2 -= prices_series[dates[i - 50]]
                    curr_sum2 += prices_series[dates[i]]
                    avg2 = curr_sum1 / 50 

                    MA50[date] = avg2


                    if avg1 > avg2: 
                        # buy ticker 
                        cost = price_series[dates[i]]

                        if cost <= self.cash: 
                            self.cash -= cost 
                            self.portfolio[ticker] = 1
                
                self._record (date, price_data)
                         




