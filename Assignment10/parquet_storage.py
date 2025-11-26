from data_loader import DataLoader
import pandas as pd
import pyspark
import pyarrow.parquet as pq
import numpy as np


data = DataLoader('market_data_multi.csv','tickers.csv')

# data.market_data.to_parquet('/market_data/market_data_multi.parquet')
filepath = 'Assignment10/market_data/market_data_multi.parquet'

# data.tickers.to_parquet('Assignment10/market_data/tickers.parquet')

# market_data = pd.read_parquet('Assignment10/market_data/market_data_multi.parquet')
# tickers = pd.read_parquet('Assignment10/market_data/tickers.parquet')

start = '2025-11-17 09:30:00'
end = '2025-11-18 16:00:00'

dfs = {}
for ticker in data.tickers['ticker']:
    dfs[ticker] = pd.read_parquet(filepath, filters=[('ticker', '==', ticker)])

full_df = pd.read_parquet(filepath)
# dataset = pq.ParquetDataset(filepath, filters=[('ticker', '==', 'AAPL')])
AAPL_df = dfs['AAPL']
AAPL_df = AAPL_df[(AAPL_df['timestamp'] >= start) & (AAPL_df['timestamp'] <= end)]

AAPL_df['Minute Returns'] = AAPL_df['close'].pct_change()
AAPL_df['5 Minutes Returns'] = (1+AAPL_df['Minute Returns']).rolling(window=5).apply(np.prod, raw=True) - 1

print(AAPL_df)

vols = {}
for df in dfs:
    vols[df] = float(dfs[df]['close'].diff().std()-1)

print(vols)