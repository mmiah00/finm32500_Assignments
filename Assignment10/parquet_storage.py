from data_loader import DataLoader
import pandas as pd
import pyspark
import pyarrow.parquet as pq


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

dataset = pq.ParquetDataset(filepath, filters=[('ticker', '==', 'AAPL')])
AAPL_df = dataset.read().to_pandas()
AAPL_df = AAPL_df[(AAPL_df['timestamp'] >= start) & (AAPL_df['timestamp'] <= end)]

