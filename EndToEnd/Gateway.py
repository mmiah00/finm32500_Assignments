import pandas as pd

global MESSAGE_DELIMITER
MESSAGE_DELIMITER = "*_*"

class Gateway:
    def __init__(self, df, ticker):
        self.df = df
        self.ticker = ticker

    def stream_data(self):
        market_data = {}
        for index, row in self.df.iterrows():
            market_data[row['Datetime']] = {'Ticker': self.ticker, 'Price': row['Close']}
        return market_data



