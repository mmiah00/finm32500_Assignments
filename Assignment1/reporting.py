from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from engine import ExecutionEngine

def find_total_return (marketdatapoints): 
    total  = 0 

    prev_order = marketdatapoints[0] 
    
    for i in range (1, len(marketdatapoints)): 
        curr_order = marketdatapoints[i] 
        simple_return = (curr_order.price - prev_order.price - 0.0) / prev_order.price
        total += simple_return 

        prev_order = curr_order 

    return total  


def periodic_returns(marketdatapoints): 
    # periodic return = ((end_val / beg_val) - 1) * 100% 

    periodic_returns = [] 

    prev_order = marketdatapoints[0] 

    for i in range (1, len(marketdatapoints)): 
        curr_order = marketdatapoints[i] 

        calc = ((curr_order.price / prev_order.price) - 1) # * 100 if i want to find the percentage, otherwise leave between 0-1 
        periodic_returns.append(calc) 
        
        prev_order = curr_order

    return periodic_returns  

def calc_sharpe_ratio(marketdatapoints, periodic_returns): 
    num_datapoints = len(marketdatapoints)

    Rp = 0 # Portfolio's Average Return (Rp) 
    Rf = 0.0389 # Risk-Free Rate (Rf), for our purposes we will use the yield on a 3-month U.S. Treasury bill as the risk-free rate. The current 3 Month Treasury Bill Rate, as of September 19, 2025, is 3.89%
    sigma = 0 # aka Portfolio's standard deviation, measures the volatility or risk of the investment's returns over time 

    # calculate Portfolio's Average Return (Rp)  
    for ret in periodic_returns: 
        Rp += ret 
    
    Rp /= num_datapoints 

    # calculate Sigma 
    mean_return = find_total_return (marketdatapoints) / num_datapoints
    
    for mdp in marketdatapoints: 
        sigma += (mdp - mean_return) ** 2 # calculate squared variances for each data point 
    
    sigma /= num_datapoints # at this point we have the variance (sigma^2)
    sigma ** 0.5 # take square root to find the stanadard deviation 

    return (Rp - Rf) / sigma 
    


def max_drawdown (marketdatapoints): 
    mdd = 0 

    portfolio_val = marketdatapoints[0].price 

    peak = float('-inf')
    trough = float('inf')

    for order in orders: 
        if order.side == "BUY": 
            # a trough 
            portfolio_val = portfolio_val - order.price * quantity
            trough = min (trough, portfolio_val)
        else: 
            # a peak 
            portfolio_val = portfolio_val + order.price * quantity
            peak = max (peak, portfolio_val)

    mdd = (trough - peak)/peak

    return mdd 

def save_equity_plot(marketdatapoints, filename="equity_curve.png"):
    y = [] 

    portfolio_val = 0 

    for order in orders: 
        if order.side == "BUY": 
            portfolio_val = portfolio_val - order.price * quantity
        else: 
            portfolio_val = portfolio_val + order.price * quantity
        y.append(portfolio_val)


    plt.figure(figsize=(8,4))
    y.plot(title="Equity Curve")
    plt.ylabel("Equity Value")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def write_markdown_report(marketdatapoints, outpath="performance.md"):
    total_return = find_total_return (marketdatapoints)
    sharpe = calc_sharpe_ratio (marketdatapoints)
    max_dd = max_drawdown (marketdatapoints)

    periodic_returns = periodic_returns(marketdatapoints)
    periodic_returns = pd.DataFrame(periodic_returns) # converting from a list to a Pandas Dataframe

    img_path = save_equity_plot(marketdatapoints)

    with open(outpath, "w") as f:
        f.write("# Backtest Performance Report\n\n")
        f.write("## Key Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------:|\n")
        f.write(f"| Total Return | {total_return:.2%} |\n")
        f.write(f"| Sharpe Ratio (annualized) | {sharpe:.2f} |\n")
        f.write(f"| Max Drawdown | {max_dd:.2%} |\n\n")

        f.write("## Equity Curve\n\n")
        f.write(f"![Equity Curve]({img_path})\n\n")

        f.write("## Periodic Returns (summary)\n\n")
        f.write(periodic_returns.describe().to_markdown() + "\n\n")


    return outpath