import sqlite3
import pandas as pd
import numpy as np

from sqlite_storage import (
    create_schema,
    insert_data,
    get_data_for_ticker,
    get_avg_daily_volume,
)


def _sample_df():
    data = {
        "timestamp": pd.to_datetime(
            [
                "2024-01-02 09:30:00",
                "2024-01-02 09:30:00",
                "2024-01-03 09:30:00",
                "2024-01-03 09:30:00",
            ]
        ),
        "ticker": ["AAPL", "MSFT", "AAPL", "MSFT"],
        "open": [100, 200, 101, 201],
        "high": [101, 202, 103, 203],
        "low": [99, 199, 100, 200],
        "close": [100.5, 201, 102, 202],
        "volume": [1000, 1500, 1100, 1600],
    }
    return pd.DataFrame(data)


def test_create_schema_and_insert_data():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)

    df = _sample_df()
    insert_data(conn, df)

    # check tables exist and row counts
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = {row[0] for row in cur.fetchall()}
    assert "tickers" in table_names
    assert "prices" in table_names

    # tickers table should have 2 rows
    cur.execute("SELECT COUNT(*) FROM tickers")
    assert cur.fetchone()[0] == 2

    # prices table should have 4 rows
    cur.execute("SELECT COUNT(*) FROM prices")
    assert cur.fetchone()[0] == len(df)


def test_get_data_for_ticker_filters_correctly():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    df = _sample_df()
    insert_data(conn, df)

    result = get_data_for_ticker(
        conn,
        ticker="AAPL",
        start="2024-01-02",
        end="2024-01-03",  # inclusive or exclusive depends on your impl
    )

    # Only AAPL rows in range
    assert set(result["ticker"].unique()) == {"AAPL"}
    # There should be 2 rows for AAPL in the sample data
    assert len(result) == 2


def test_get_avg_daily_volume():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    df = _sample_df()
    insert_data(conn, df)

    avg_vol = get_avg_daily_volume(conn)  # expect something like columns: ticker, avg_volume

    # turn into dict: {ticker: avg_volume}
    vol_dict = dict(zip(avg_vol["ticker"], avg_vol["avg_volume"]))

    # manually compute expected averages
    expected = (
        df.groupby("ticker")["volume"].mean().to_dict()
    )

    # check equality with tolerance
    for t in expected:
        assert np.isclose(vol_dict[t], expected[t])
