import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class FeatureEngineering:
    def __init__(self, folder='./Assignment11/'):
        self.folder = folder
        self.marketfile = 'market_data_ml.csv'
        self.tickersfile = 'tickers-1.csv'
        self.market_data_df = pd.read_csv(self.folder + self.marketfile, parse_dates=True, index_col=0)
        self.tickers_df = pd.read_csv(self.folder + self.tickersfile)

    def run(self):
        df = self.market_data_df
        df['1 day'] = df.groupby('ticker')['close'].pct_change(1)
        df['3 day'] = df.groupby('ticker')['close'].pct_change(3)
        df['5 day'] = df.groupby('ticker')['close'].pct_change(5)
        df['SMA 5'] = df.groupby('ticker')['close'].pct_change().rolling(5).mean()
        df['SMA 10'] = df.groupby('ticker')['close'].pct_change().rolling(10).mean()
        df['RSI'] = df.groupby('ticker')['close'].transform(
            lambda prices, period=14:
                100 - (100 / (1 + prices.diff().clip(lower=0).ewm(com=period-1, adjust=False).mean()
                              / -prices.diff().clip(upper=0).ewm(com=period-1, adjust=False).mean()))
        )

        df['Signal Line'] = (
            df.groupby('ticker')['close']
              .transform(lambda x: x.ewm(span=12, adjust=False).mean()
                                   - x.ewm(span=26, adjust=False).mean())
              .groupby(df['ticker'])
              .transform(lambda x: x.ewm(span=9, adjust=False).mean())
        )

        df['Z-score'] = df.groupby('ticker')['close'].transform(
            lambda x: (x - x.mean()) / x.std()
        )

        df['Label'] = df.groupby('ticker')['1 day'].transform(
            lambda x: (x.shift(-1) > 0).astype(int)
        )

        self.market_data_df = df
        return self.market_data_df


if __name__ == "__main__":
    fe = FeatureEngineering()
    market_data_df = fe.run()
    print(market_data_df.head())
    # To plot:
    # market_data_df[market_data_df.ticker == 'AAPL']['RSI'].plot()
    # plt.tight_layout()
    # plt.show()
