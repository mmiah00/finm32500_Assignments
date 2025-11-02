'''
Task: Compute rolling metrics per symbol:
20-period moving average
20-period rolling standard deviation
Rolling Sharpe ratio (assume risk-free rate = 0)
Expectations:
Implement using both pandas and polars.
Time each computation and compare performance.
Visualize results for one symbol (e.g., AAPL) using matplotlib or plotly.
Discuss syntax differences and performance tradeoffs.
'''
import pandas as pd 
import polars as pl
import datetime
from memory_profiler import profile
from data_loader import pandas_df, polars_df 
import matplotlib as plt 

tickers = polars_df['symbol'].unique() 

##########################################################################################

# Computing metrics using pandas(pd) 

@profile
def calc_MA_pd (symbol, df):
    # calculates 20-period moving average per symbol 
    df["Moving_MA"] = df[symbol].rolling(window=20).mean()

    return df 

@profile
def calc_rolling_std_pd (symbol, df, window=20):
    # calculates 20-period moving average per symbol 
    df["Rolling Std"] = df[symbol].rolling(window=20).std()

    return df 

@profile
def calc_rolling_sharpe_pd (symbol, df, window=20): 
    df["Rolling Sharpe"] = df['Moving_MA']/df['Rolling Std']
    return df

##########################################################################################

# Computing metrics using pandas(pd) 

@profile
def calc_MA_pl (symbol, df):
    # calculates 20-period moving average per symbol 
    new_df = df.with_columns(
        df[symbol].rolling_mean(window_size=window).alias("ma_20")
    )

    return new_df 

@profile
def calc_rolling_std_pl (symbol, df, window=20):
    # calculates 20-period moving average per symbol 
    new_df = df.with_columns(
        df[symbol].rolling_std(window_size=window).alias("std_20")
    )

    return new_df 

@profile
def calc_rolling_sharpe_pl (symbol, df, window=20): 
    new_df = df.with_columns(
        (df["rolling_mean"] / df["rolling_std"]).alias("rolling_sharpe")
    )
    return new_df

##########################################################################################

# Visualize results for one symbol (e.g., AAPL) using matplotlib or plotly.

@profile
def display_MA_plot(df, symbol):    
    plt.plot(df.index, df[symbol]["Moving_MA"])

calc_MA_pd ("AAPL", pandas_df)
calc_MA_pl ("AAPL", polars_df) 

calc_rolling_std_pd ("AAPL", pandas_df)
calc_rolling_std_pl ("AAPL", polars_df)

calc_rolling_sharpe_pd ("AAPL", pandas_df)
calc_rolling_sharpe_pl ("AAPL", polars_df) 

display_MA_plot(pandas_df, "AAPL")
display_MA_plot(polars_df, "AAPL")

