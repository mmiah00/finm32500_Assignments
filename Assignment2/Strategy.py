import pandas as pd

class Strategy:
    def __init__(self, initial_cash=1_000_000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.portfolio = {}  # ticker -> shares held
        self.history = []    # track (date, portfolio_value, cash, holdings_value)

    def run(self, price_data):
        """
        Run the strategy. Must be implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement run()")

    def _record(self, date, price_data):
        """Helper: record portfolio value on a given date."""
        holdings_value = 0
        for ticker, shares in self.portfolio.items():
            price = price_data[ticker][date]
            holdings_value += shares*price

        total_value = self.cash + holdings_value
        self.history.append((date, total_value, self.cash, holdings_value))
    
    def _buy(self, ticker, ticker_price, amount, date):
        cost = ticker_price * amount 

        if cost <= self.cash: 
            self.cash -= cost 
            self.portfolio[ticker] = self.portfolio.get(ticker, 0) + amount
        else: 
            raise ValueError(f"Not enough cash to buy {amount} shares of {ticker}. Cash amount: {self.cash}. Purchase attempted: {cost}.") 

    def get_results(self):
        """Return portfolio performance as a DataFrame."""
        return pd.DataFrame(self.history, columns=["Date", "Portfolio Value", "Cash", "HoldingsValue"]).set_index("Date")
