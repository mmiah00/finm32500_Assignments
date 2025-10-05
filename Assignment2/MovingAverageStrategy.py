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
        for ticker, price_series in price_data.items(): 
            rolling_avgs20 = price_series.rolling(window=20).mean()
            rolling_avgs50 = price_series.rolling(window=50).mean()
            dates = price_series.index 

            for i in range(len(rolling_avgs20)): 
                if rolling_avgs20.iloc[i] > rolling_avgs50.iloc[i]: 
                    # buy ticker 
                    
                    try: 
                        self._buy(ticker, price_series.iloc[i], 1, dates[i])
                        print (f"MA20 for {ticker} on day {dates[i]} ({rolling_avgs20.iloc[i]}) is greater than MA50 for {ticker} on day {dates[i]} ({rolling_avgs50.iloc[i]}). Buying signal.")
                        self._record (dates[i], price_data)
                    except Exception as e: 
                        print (f"Not enough cash to make purchase of 1 share of {ticker} on {dates[i]}. Current cash balance: {self.cash}. Attempted purchase: {price_series.iloc[i]}")
            print()





        '''
        MA20 = {} # key = ticker, value = dict (key = date, value = 20-day moving average value)  
        MA50 = {} # key = ticker, value = dict (key = date, value = 50-day moving average value)  
        sums = {} # key = ticker, value = list -> [sum for ma20, sum for ma50]

        dates = None 
        tickers = []

        for ticker, price_series in price_data.items(): 
            if type(dates) != pd.Series: 
                dates = price_series.index #price_series['Date']
            tickers.append(ticker) 
            MA20[ticker] = {} 
            MA50[ticker] = {} 
            sums[ticker] = [0,0]

        for i in range (len(dates)): 
            print("=========================================================")
            day = i + 1 # day 1 is at index 0, and so on 
            date = dates[i] 

            print(f"Today is day {day}, {date}.")

            for t in tickers: 
                todays_price = price_data[t][date]

                if day < 20: 
                    sums[t][0] += todays_price
                    sums[t][1] += todays_price
                
                elif day == 20: 
                    sums[t][0] += todays_price
                    avg = sums[t][0] / 20 
                    MA20[t][date] = avg 

                    sums[t][1] += todays_price
                
                elif day > 20 and day < 50: 
                    sums[t][0] += todays_price
                    sums[t][0] -= price_data[t][dates[i-20]]
                    avg = sums[t][0] / 20 
                    MA20[t][date] = avg 

                    sums[t][1] += todays_price
                
                else: 
                    sums[t][0] += todays_price
                    sums[t][0] -= price_data[t][dates[i-20]]
                    avg1 = sums[t][0] / 20 
                    MA20[t][date] = avg1 

                    sums[t][1] += todays_price
                    sums[t][1] -= price_data[t][dates[i-50]]
                    avg2 = sums[t][1] / 50 
                    MA50[t][date] = avg2

                    if avg1 > avg2: 
                        # buy ticker 
                        try: 
                            price = price_data[t][dates[i]]
                            self._buy(t, price, 1, dates[i])
                            print(f"MA20 ({avg1}) is greater than MA50 ({avg2}). Buying 1 share of {t} on day {day} ({date}).")
                            print() 
                        except ValueError as e: 
                            print (f"Couldn't buy 1 share of {t} at price {price}. Not enough cash.")

            self._record (date, price_data)
            print("=========================================================")    
        '''



        '''
        for ticker, price_series in price_data.items(): 
            print(f"Calculating MA for {ticker}")
            if type(dates) != pd.Series: 
                dates = price_series.index #price_series['Date']
            
            MA20 = {} # key = date, value = 20-day moving average value 
            MA50 = {} # key = date, value = 50-day moving average value 

            curr_sum1 = 0 # keeping track of average for 20 day MA
            curr_sum2 = 0 # keeping track of average for 50 day MA 

            for i in range(len(dates)): 
                day = i + 1 
                date = dates[i]

                print(f"Today is day {day}: {date}")

                if day < 20: 
                    print (f"Adding {price_series[dates[i]]} to sum20 and sum50.")
                    curr_sum1 += price_series[dates[i]]
                    curr_sum2 += price_series[dates[i]]

                elif day == 20: 
                    curr_sum1 += price_series[dates[i]]
                    avg = curr_sum1 / 20 
                    MA20[date] = avg 

                    print (f"Adding {price_series[dates[i]]} to sum20 and sum50. MA20 of day {day} is {avg}.")

                    curr_sum2 += price_series[dates[i]]

                elif day >= 20 and day < 50: 
                    # cant find ma50 for days 20-50, only ma20 
                    # subtract price at day (day - 20) and find the average
                    # update MA20 dict 
                    curr_sum1 -= price_series[dates[i - 20]]
                    curr_sum1 += price_series[dates[i]]
                    avg = curr_sum1 / 20 

                    print (f"Adding {price_series[dates[i]]} to sum20 and sum50. Subtracting price from day {i - 20}: {price_series[dates[i - 20]]}. MA20 of day {day} is {avg}.")

                    MA20[date] = avg 

                    curr_sum2 += price_series[dates[i]]

                else: 
                    # can find ma50 for days >50
                    # subtract price at day (day - 20) to find ma20 
                    # subtract price at day (day - 50) to find ma50 
                    # find average of each 
                    # update MA20 and MA50 
                    # compare the prices and trade is MA20 > MA50 
                    curr_sum1 -= price_series[dates[i - 20]]
                    curr_sum1 += price_series[dates[i]]
                    avg1 = curr_sum1 / 20 

                    MA20[date] = avg1 

                    curr_sum2 -= price_series[dates[i - 50]]
                    curr_sum2 += price_series[dates[i]]
                    avg2 = curr_sum1 / 50 

                    MA50[date] = avg2

                    print (f"Adding {price_series[dates[i]]} to sum20. Subtracting price from day {i - 20}: {price_series[dates[i - 20]]} for sum20. MA20 of day {day} is {avg}.")
                    print (f"Adding {price_series[dates[i]]} to sum50. Subtracting price from day {i - 50}: {price_series[dates[i - 50]]} for sum50. MA50 of day {day} is {avg}.")
                    
                    if avg1 > avg2: 
                        # buy ticker 
                        cost = price_series[dates[i]]

                        if cost <= self.cash: 
                            self.cash -= cost 
                            self.portfolio[ticker] = 1
                            print(f"MA20 is greater than MA50. Buying 1 share of {ticker} on day {day} ({date}).")
                print() 

                self._record (date, price_data)
        '''        




