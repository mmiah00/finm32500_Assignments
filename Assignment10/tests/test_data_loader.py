import pandas as pd
import numpy as np
from pathlib import Path
import pytest

from data_loader import load_market_data


def test_load_market_data_validates_and_normalizes(tmp_path):
    # --- create fake market_data_multi.csv ---
    market_path = tmp_path / "market_data_multi.csv"
    market_csv = """timestamp,ticker,open,high,low,close,volume
2024-01-02 09:30:00,AAPL,100,101,99,100.5,1000
2024-01-02 09:30:00,MSFT,200,202,199,201,1500
2024-01-03 09:30:00,AAPL,101,103,100,102,1100
2024-01-03 09:30:00,MSFT,201,203,200,202,1600
"""
    market_path.write_text(market_csv)

    # --- create fake tickers.csv ---
    tickers_path = tmp_path / "tickers.csv"
    tickers_csv = """symbol
AAPL
MSFT
"""
    tickers_path.write_text(tickers_csv)

    # --- call your loader ---
    df = load_market_data(market_path, tickers_path)

    # 1) Check columns normalized
    expected_cols = {"timestamp", "ticker", "open", "high", "low", "close", "volume"}
    assert set(df.columns) == expected_cols

    # 2) Check datetime type
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])

    # 3) No missing timestamps or prices
    price_cols = ["open", "high", "low", "close"]
    assert not df["timestamp"].isna().any()
    assert not df[price_cols].isna().any().any()

    # 4) All tickers from tickers.csv are present
    tickers_list = pd.read_csv(tickers_path)["symbol"].unique()
    df_tickers = df["ticker"].unique()
    for t in tickers_list:
        assert t in df_tickers

def test_load_market_data_raises_on_missing_prices(tmp_path):
    market_path = tmp_path / "market_data_multi.csv"
    market_csv = """timestamp,ticker,open,high,low,close,volume
2024-01-02 09:30:00,AAPL,100,101,99,,1000
"""
    market_path.write_text(market_csv)

    tickers_path = tmp_path / "tickers.csv"
    tickers_path.write_text("symbol\nAAPL\n")

    with pytest.raises(ValueError):
        load_market_data(market_path, tickers_path)
