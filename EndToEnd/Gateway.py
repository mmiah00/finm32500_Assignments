'''
Gateway - Write all orders to a file for audit and analysis. This should include when orders are sent, modified, cancelled or filled. 
Implementation Target:

An OrderManager class for validation and a Gateway class for logging orders.
'''

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
    
    def log_order(self, order, action):
        log_entry = f"{order.time}{MESSAGE_DELIMITER}{order.order_id}{MESSAGE_DELIMITER}{order.side}{MESSAGE_DELIMITER}{order.price}{MESSAGE_DELIMITER}{order.size}{MESSAGE_DELIMITER}{action}\n"
        with open('order_log.txt', 'a') as f:
            f.write(log_entry)