import pandas as pd

class DataLoader:
    def __init__(self, market_data_fp, tickers_fp):
        self.market_data = self._load_data(market_data_fp)
        self.tickers = self._load_data(tickers_fp)
        self._no_missing_values()
        self._verify_tickers()
        self._normalize_columns()

    def _load_data(self, filepath):
        folder = 'Assignment10/market_data/'
        df = pd.read_csv(folder+filepath)
        return df
    
    def _no_missing_values(self):
        return self.market_data.dropna()
    
    def _verify_tickers(self):
        valid_tickers = self.market_data['ticker'].isin(self.tickers['symbol'])
        self.market_data = self.market_data[valid_tickers]
        return self.market_data
    
    def _normalize_columns(self):
        self.tickers = self.tickers.rename(columns={'symbol': 'ticker'})

    def _datetime(self):
        self.market_data = pd.to_datetime(self.market_data['timestamp'])


data = DataLoader('market_data_multi.csv','tickers.csv')

