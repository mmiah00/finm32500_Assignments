import pandas as pd
import json
import multiprocessing
import concurrent.futures
from memory_profiler import profile
from data_loader import polars_df, pandas_df

with open("data/portfolio_structure-1.json", "r") as file:
    data = json.load(file)


for position in data["positions"]:
    value = position["quantity"] * position["price"]
    print(value)


# sequential 
def calc_metrics_seq_pandas(df, symbol, qty=1):
    '''
    value = quantity × latest price
    volatility = rolling standard deviation of returns
    drawdown = maximum peak-to-trough loss
    '''
    filtered_df = df[df['symbol'] == symbol]
    latest_price = filtered_df.iloc[-1]
    filtered_df['value'] = qty * latest_price 
    filtered_df['returns'] = filtered_df["price"].pct_change() 
    filtered_df['volatility'] = filtered_df['returns'].rolling(window=20).std()

    cumulative_returns = (1 + filtered_df['returns']).cumprod() - 1
    filtered_df['drawdown'] = (cumulative_returns - cumulative_returns.cummax()) / cumulative_returns.cummax()

    return filtered_df

def calc_metrics_seq_polars(df, symbol, qty=1):
    '''
    value = quantity × latest price
    volatility = rolling standard deviation of returns
    drawdown = maximum peak-to-trough loss
    '''
    filtered_df = df[df['symbol'] == symbol]
    latest_price = filtered_df.iloc[-1]
    filtered_df['value'] = qty * latest_price 
    filtered_df['returns'] = filtered_df["price"].pct_change() 
    filtered_df['volatility'] = filtered_df['returns'].rolling(window=20).std()

    cumulative_returns = (1 + filtered_df['returns']).cumprod() - 1
    filtered_df['drawdown'] = (cumulative_returns - cumulative_returns.cummax()) / cumulative_returns.cummax()

    return filtered_df

calc_metrics_seq_pandas(pandas_df, "AAPL") 
calc_metrics_seq_polars(polars_df, "AAPL") 
workers = len(data["positions"])

# parallel 

@profile 
def processing_pandas():
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        executor.submit(calc_metrics_seq_pandas, workers)
        results.append(executor.map(calc_metrics_seq_pandas, results))

@profile 
def processing_polars():
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        executor.submit(calc_metrics_seq_polars, workers)
        results.append(executor.map(calc_metrics_seq_polars, results))

filtered_df_pandas = calc_metrics_seq_pandas(pandas_df, "AAPL")
filtered_df_polars = calc_metrics_seq_polars(polars_df, "AAPL")

if __name__ == '__main__':
    processing_pandas()
    processing_polars()
    filtered_df_pandas.to_json('part4_pandas.json') 
    filtered_df_polars.to_json('part4_polars.json')

