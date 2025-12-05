import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

load_dotenv()


class AlpacaDataFetcher:
    """Fetches live AAPL data from Alpaca, cleans it, and stores in CSV format."""
    
    def __init__(self, ticker="AAPL", timeframe_minutes=45):
        """
        Initialize Alpaca connection.
        
        Args:
            ticker: Stock ticker symbol (default: AAPL)
            timeframe_minutes: Candle interval in minutes (default: 45)
        """
        self.ticker = ticker
        self.timeframe_minutes = timeframe_minutes
        self.api = tradeapi.REST(
            key_id=os.getenv('KEY_ID'),
            secret_key=os.getenv('SECRET_KEY'),
            base_url='https://paper-api.alpaca.markets',
            api_version='v2'
        )
        
        # Setup paths
        self.base_path = Path(__file__).resolve().parent
        self.cleaned_dir = self.base_path / 'cleaned'
        self.cleaned_dir.mkdir(exist_ok=True)
        self.csv_filename = f'{self.ticker}_live.csv'
        self.csv_path = self.cleaned_dir / self.csv_filename
    
    def fetch_latest_bars(self, lookback_days=7):
        """
        Fetch latest bars from Alpaca for the given lookback period.
        Uses IEX data source (free tier) instead of SIP.
        
        Args:
            lookback_days: Number of days to fetch (default: 7)
        
        Returns:
            DataFrame with Open, High, Low, Close, Volume
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)
        
        print(f"Fetching {self.ticker} data from {start_date} to {end_date} (IEX feed)...")
        
        try:
            bars = self.api.get_bars(
                self.ticker,
                TimeFrame(self.timeframe_minutes, TimeFrameUnit.Minute),
                start=str(start_date),
                end=str(end_date),
                adjustment='raw',
                feed='iex'  # Use IEX feed instead of SIP (free tier)
            )
            df = bars.df
            print(f"Successfully fetched {len(df)} bars")
            return df
        except Exception as e:
            print(f"Error fetching data from Alpaca: {e}")
            print("Trying alternative with daily data...")
            return self.fetch_daily_bars(lookback_days)
    
    def fetch_daily_bars(self, lookback_days=7):
        """
        Fallback: fetch daily bars if minute bars fail.
        
        Args:
            lookback_days: Number of days to fetch (default: 7)
        
        Returns:
            DataFrame with Open, High, Low, Close, Volume
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)
        
        print(f"Fetching daily {self.ticker} data from {start_date} to {end_date}...")
        
        try:
            bars = self.api.get_bars(
                self.ticker,
                TimeFrame(1, TimeFrameUnit.Day),
                start=str(start_date),
                end=str(end_date),
                adjustment='raw',
                feed='iex'
            )
            df = bars.df
            print(f"Successfully fetched {len(df)} daily bars")
            return df
        except Exception as e:
            print(f"Error fetching daily data from Alpaca: {e}")
            return None
    
    def process_data(self, df):
        """
        Process raw OHLCV data with derived features for momentum strategy.
        
        Args:
            df: Raw OHLC dataframe
        
        Returns:
            Cleaned dataframe with technical indicators
        """
        if df is None or df.empty:
            print("No data to process")
            return None
        
        # Reset index to make timestamp a column
        df = df.reset_index()
        df.rename(columns={'timestamp': 'Datetime'}, inplace=True)
        
        # Ensure Datetime is datetime type
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df = df.sort_values('Datetime')
        
        # Keep only required columns
        df = df[['Datetime', 'open', 'high', 'low', 'close', 'volume']].copy()
        df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Remove NaN values
        df = df.dropna()
        df = df.drop_duplicates()
        
        # Derived features for momentum strategy
        df['Minute Returns'] = df['Close'].pct_change()
        df['Rolling 5 Minute Returns'] = (1 + df['Minute Returns']).rolling(window=5).apply(np.prod, raw=True) - 1
        df['20 Minute Moving Average'] = df['Close'].rolling(window=20).mean()
        df['50 Minute Moving Average'] = df['Close'].rolling(window=50).mean()
        
        print(f"Processed data shape: {df.shape}")
        print(f"Data columns: {df.columns.tolist()}")
        
        return df
    
    def save_to_csv(self, df):
        """
        Save processed data to CSV file for trading.
        
        Args:
            df: Processed dataframe
        
        Returns:
            Path to saved CSV file
        """
        if df is None or df.empty:
            print("No data to save")
            return None
        
        try:
            df.to_csv(self.csv_path, index=False)
            print(f"Data saved to {self.csv_path}")
            return str(self.csv_path)
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return None
    
    def fetch_and_save(self, lookback_days=7):
        """
        Complete pipeline: fetch from Alpaca, process, and save to CSV.
        
        Args:
            lookback_days: Number of days to fetch (default: 7)
        
        Returns:
            Path to saved CSV or None if failed
        """
        df = self.fetch_latest_bars(lookback_days)
        df = self.process_data(df)
        csv_path = self.save_to_csv(df)
        return csv_path


if __name__ == "__main__":
    # Example usage
    fetcher = AlpacaDataFetcher(ticker="AAPL", timeframe_minutes=5)
    csv_path = fetcher.fetch_and_save(lookback_days=7)
    if csv_path:
        print(f"Ready to trade with data from: {csv_path}")
