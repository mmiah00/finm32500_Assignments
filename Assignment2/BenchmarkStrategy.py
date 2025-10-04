import pandas as pd
from Strategy import Strategy

class BenchmarkStrategy(Strategy):
    def __init__(self, initial_cash=1000000, shares=5, allocation_per_ticker=None, max_participation=0.05):
        """
        Benchmark Strategy
        - Buy X shares OR allocate fixed $ amount per ticker (on first day only).
        - Hold until the end, no further trades. 
        
        Args:
            initial_cash: starting cash
            shares: number of shares to buy per ticker (if None, use allocation_per_ticker)
            allocation_per_ticker: fixed $ allocation per ticker (overrides shares if given)
            max_participation: maximum % of daily ADV (default 5%)
        """
        super().__init__(initial_cash)
        self.shares = shares # num shares 
        self.allocation_per_ticker = allocation_per_ticker
        self.max_participation = max_participation

    def run(self, price_data, start_date="2005-01-03"):
        """
        Args: 
            price_data: dictionary generated in PriceLoader.py, key = ticker name (str) and value = ticker prices (Pandas Series)
            start_date: date we are trading on (should be the first day only)
        """
        dates = None 

        print("Running Benchmark Strategy...")
        for ticker, price_series in price_data.items(): 
            
            price = price_series[start_date] 

            if type(dates) != pd.Series: 
                dates = price_series.index #price_series['Date']

            X = self.shares # num shares 

            if self.allocation_per_ticker: 
                # fixed dollar allocation per ticker 
                X = int(self.allocation_per_ticker // open_price)
            
            if price == None or X == None : 
                continue 

            print(f"Buying {X} shares of {ticker} at price {price}.")

            cost = price * X 

            if cost <= self.cash: 
                self.cash -= cost 
                self.portfolio[ticker] = X 
            
        self._record (start_date, price_data)

        for date in dates: 
            if date != start_date: 
                self._record(date, price_data)

