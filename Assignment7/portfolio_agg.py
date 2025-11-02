import pandas as pd
import json

with open("data/portfolio_structure-1.json", "r") as file:
    data = json.load(file)


for position in data["positions"]:
    value = position["quantity"] * position["price"]
    print(value)

# sequential 
def calc_metrics_seq (df, symbol, qty=1):
    '''
    value = quantity × latest price
    volatility = rolling standard deviation of returns
    drawdown = maximum peak-to-trough loss
    '''
    latest_price = df[symbol].sort()[-1] 
    df['value'] = qty * latest_price 

    df['returns'] = df[symbol].pct_change() 
    df['volatility'] = df['returns'].rolling(window=20).std()

    cumulative_returns = (1 + df['returns']).cumprod() - 1
    df['drawdown'] = (cumulative_returns - cumulative_returns.cummax()) / cumulative_returns.cummax()

    return df

calc_metrics_seq() 

# parallel 


