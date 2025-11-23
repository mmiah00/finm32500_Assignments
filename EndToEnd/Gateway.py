import pandas as pd

global MESSAGE_DELIMITER
MESSAGE_DELIMITER = "*_*"

# class Gateway:
#     def __init__(self, df, ticker):
#         self.df = df
#         self.ticker = ticker

#     def stream_data(self):
#         market_data = {}
#         for index, row in self.df.iterrows():
#             market_data[row['Datetime']] = {'Ticker': self.ticker, 'Price': row['Close']}
#         return market_data


class Gateway:
    def __init__(self, csv_fp):
        # Read cleaned CSV files from Part 1.
        self.df = pd.read_csv(csv_fp)
        self.ticker = os.path.basename(csv_fp).split('_')[0]

    def stream_data(self):
        market_data = {}
        for index, row in self.df.iterrows():
            market_data[row['Datetime']] = {'Ticker': self.ticker, 'Price': row['Close']}
        return market_data