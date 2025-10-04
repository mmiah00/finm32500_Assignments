import pandas as pd
from Strategy import Strategy

class BenchmarkStrategy(Strategy):
    def __init__(self, initial_cash=1000000, shares=None, allocation_per_ticker=None, max_participation=0.05):
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

    def run(self, price_data):
        # price_data is a dataframe with columns 

        def sort_dates (): 
            dates = set() 

            for df in price_data: 
                dates.add(df.index)
            
            dates = sorted(dates) # O(n log n)

            return dates 

        dates = sort_dates() 
        first_day = dates[0] 

        for df in price_data: 



        for ticker, df in price_data.items():
            if first_day not in df.index:
                continue

            open_price = df.loc[first_day, "Open"]
            adv = df["Volume"].rolling(20, min_periods=1).mean().iloc[0]  # proxy ADV
            max_shares = int(self.max_participation * adv)

            if self.allocation_per_ticker is not None:
                # Fixed dollar allocation per ticker
                shares_to_buy = int(self.allocation_per_ticker // open_price)
            elif self.shares is not None:
                # Fixed X shares
                shares_to_buy = self.shares
            else:
                # Default: equal-weight allocation across all tickers
                shares_to_buy = int((self.initial_cash / len(price_data)) // open_price)

            # Enforce participation cap
            shares_to_buy = min(shares_to_buy, max_shares)

            cost = shares_to_buy * open_price
            if cost <= self.cash and shares_to_buy > 0:
                self.cash -= cost
                self.portfolio[ticker] = shares_to_buy

        # --- Daily portfolio valuation ---
        for date in all_dates:
            self._record(date, price_data)
