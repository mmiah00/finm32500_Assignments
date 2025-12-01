import pandas as pd
from pathlib import Path

from parquet_storage import write_parquet, load_ticker_range


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


def test_write_parquet_partitions_by_ticker(tmp_path):
    df = _sample_df()
    out_dir = tmp_path / "market_data"
    write_parquet(df, out_dir)

    # check that partition dirs exist (e.g. ticker=AAPL, ticker=MSFT)
    partitions = [p.name for p in out_dir.rglob("*") if p.is_dir()]
    # Depending on implementation you may get just 'AAPL', 'MSFT' or 'ticker=AAPL'
    # adjust this assertion to your style:
    assert any("AAPL" in p for p in partitions)
    assert any("MSFT" in p for p in partitions)


def test_load_ticker_range_roundtrip(tmp_path):
    df = _sample_df()
    out_dir = tmp_path / "market_data"
    write_parquet(df, out_dir)

    result = load_ticker_range(
        out_dir,
        ticker="AAPL",
        start="2024-01-01",
        end="2024-01-04",
    )

    # only AAPL rows
    assert set(result["ticker"].unique()) == {"AAPL"}
    # row count matches
    assert len(result) == (df["ticker"] == "AAPL").sum()

    # sort and compare values (ignore index order)
    result_sorted = result.sort_values("timestamp").reset_index(drop=True)
    expected_sorted = df[df["ticker"] == "AAPL"].sort_values("timestamp").reset_index(drop=True)

    pd.testing.assert_frame_equal(
        result_sorted[["timestamp", "open", "high", "low", "close", "volume"]],
        expected_sorted[["timestamp", "open", "high", "low", "close", "volume"]],
    )
