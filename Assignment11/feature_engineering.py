# Problem: Prepare multi-ticker OHLCV data for modeling.

# Expectations:

# Load market_data_ml.csv and tickers.csv.
# For each ticker:
# Calculate daily returns and log returns.
# Create lag features (e.g., 1-day, 3-day, 5-day returns).
# Add technical indicators (e.g., SMA, RSI, MACD).
# Normalize or scale features as needed.
# Label data for classification (e.g., next-day return > 0 → 1, else 0) or regression.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

marketfile = 'market_data_ml.csv'
tickersfile = 'tickers-1.csv'
folder = './Assignment11/'
market_data_df = pd.read_csv(folder+marketfile, parse_dates=True, index_col=0)
tickers_df = pd.read_csv(folder+tickersfile)

market_data_df['1 day'] = market_data_df.groupby('ticker')['close'].pct_change(1)
market_data_df['3 day'] = market_data_df.groupby('ticker')['close'].pct_change(3)
market_data_df['5 day'] = market_data_df.groupby('ticker')['close'].pct_change(5)
market_data_df['SMA 5'] = market_data_df.groupby('ticker')['close'].pct_change().rolling(5).mean()
market_data_df['SMA 10'] = market_data_df.groupby('ticker')['close'].pct_change().rolling(10).mean()
market_data_df['RSI'] = market_data_df.groupby('ticker')['close'].transform(lambda prices, period=14: 100 - (100 / (1 + prices.diff().clip(lower=0).ewm(com=period-1, adjust=False).mean() / -prices.diff().clip(upper=0).ewm(com=period-1, adjust=False).mean())))
market_data_df['Signal Line'] = market_data_df.groupby('ticker')['close'].transform(lambda x: x.ewm(span=12, adjust=False).mean() - x.ewm(span=26, adjust=False).mean()).groupby(market_data_df['ticker']).transform(lambda x: x.ewm(span=9, adjust=False).mean())
market_data_df['Z-score'] = market_data_df.groupby('ticker')['close'].transform(lambda x: (x - x.mean())/x.std())
market_data_df['Label'] = market_data_df.groupby('ticker')['1 day'].transform(lambda x: (x.shift(-1) > 0).astype(int))
# print(market_data_df)
# market_data_df[market_data_df.ticker == 'AAPL']['RSI'].plot()
# plt.tight_layout()
# plt.show()