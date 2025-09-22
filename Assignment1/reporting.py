from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from engine import ExecutionEngine

# def find_total_return (engine): 
#     total  = 0 
#     marketdatapoints = engine.market_data 

#     prev_order = marketdatapoints[0] 
    
#     for i in range (1, len(marketdatapoints)): 
#         curr_order = marketdatapoints[i] 
#         simple_return = (curr_order.price - prev_order.price - 0.0) / prev_order.price
#         total += simple_return 

#         prev_order = curr_order 

#     return total  

def find_total_return (engine): 
    total = 0 

    orders = engine.order_history

    portfolio_val = engine.cash

    for order in orders: 
        if order.status == "BUY": 
            new_portfolio_val = portfolio_val - order.price * order.quantity
        else: 
            new_portfolio_val = portfolio_val + order.price * order.quantity
        
        simple_return = (new_portfolio_val - portfolio_val) / portfolio_val

        total += simple_return 
        portfolio_val = new_portfolio_val

    return total 



# def calc_periodic_returns(engine): 
#     # periodic return = ((end_val / beg_val) - 1) * 100% 

#     marketdatapoints = engine.market_data 

#     periodic_returns = [] 

#     prev_order = marketdatapoints[0] 

#     for i in range (1, len(marketdatapoints)): 
#         curr_order = marketdatapoints[i] 

#         calc = ((curr_order.price / prev_order.price) - 1) # * 100 if i want to find the percentage, otherwise leave between 0-1 
#         periodic_returns.append(calc) 
        
#         prev_order = curr_order

#     return periodic_returns  

def calc_periodic_returns(engine): 
    orders = engine.order_history

    portfolio_val = engine.cash

    periodic_returns = [] 

    for order in orders: 
        if order.status == "BUY": 
            new_portfolio_val = portfolio_val - order.price * order.quantity
        else: 
            new_portfolio_val = portfolio_val + order.price * order.quantity
        
        calc = ((new_portfolio_val / portfolio_val) - 1) 

        periodic_returns.append(calc)
        portfolio_val = new_portfolio_val

    return periodic_returns 

def calc_sharpe_ratio(engine): 
    print ("Calculating Sharpe Ratio")

    marketdatapoints = engine.market_data
    periodic_returns = calc_periodic_returns(engine)

    # num_datapoints = len(marketdatapoints) 
    num_datapoints = len(engine.order_history) 

    Rp = 0 # Portfolio's Average Return (Rp) 
    Rf = 0.0389 # Risk-Free Rate (Rf), for our purposes we will use the yield on a 3-month U.S. Treasury bill as the risk-free rate. The current 3 Month Treasury Bill Rate, as of September 19, 2025, is 3.89%
    sigma = 0 # aka Portfolio's standard deviation, measures the volatility or risk of the investment's returns over time 

    # calculate Portfolio's Average Return (Rp)  
    for ret in periodic_returns: 
        Rp += ret 
    
    Rp /= num_datapoints 

    # calculate Sigma 
    mean_return = find_total_return (engine) / num_datapoints
    print (f"Mean return: {mean_return}")
    
    for mdp in marketdatapoints: 
        sigma += (mdp.price + 0.0 - mean_return) ** 2 # calculate squared variances for each data point 
    
    sigma /= num_datapoints # at this point we have the variance (sigma^2)
    sigma = sigma ** 0.5 # take square root to find the stanadard deviation 

    print (f"Rp: {Rp}")
    print (f"Rf: {Rf}")
    print (f"sigma: {sigma}")

    return (Rp - Rf) / sigma 
    

def max_drawdown (engine): 
    mdd = 0 

    orders = engine.order_history

    portfolio_val = engine.cash

    peak = float('-inf')
    trough = float('inf')

    for order in orders: 
        if order.status == "BUY": 
            # a trough 
            portfolio_val = portfolio_val - order.price * order.quantity
            trough = min (trough, portfolio_val)
        else: 
            # a peak 
            portfolio_val = portfolio_val + order.price * order.quantity
            peak = max (peak, portfolio_val)

    mdd = (trough - peak)/peak

    return mdd 

def save_equity_plot(engine, filename="equity_curve.png"):
    x = [] 
    y = [] 

    marketdatapoints = engine.market_data 
    portfolio = engine.portfolio 

    portfolio_val = engine.cash 

    i = 0 
    for mdp in marketdatapoints: 
        x.append(i) 
        i += 1

        equity = mdp.price * portfolio[mdp.symbol] 



        if order.status == "BUY": 
            portfolio_val = portfolio_val - order.price * order.quantity
        else: 
            portfolio_val = portfolio_val + order.price * order.quantity
        
        x.append(i) 
        y.append(portfolio_val)

        i += 1


    plt.figure(figsize=(8,4))
    plt.plot(x,y)
    plt.ylabel("Equity Value")
    plt.xlabel("Time")
    plt.title('Equity Curve Plot')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename

def write_markdown_report(engine, outpath="performance.md"):
    marketdatapoints = engine.market_data 

    total_return = find_total_return (engine)
    periodic_returns = calc_periodic_returns(engine)
    sharpe = calc_sharpe_ratio (engine)
    max_dd = max_drawdown (engine)

    periodic_returns = pd.DataFrame(periodic_returns) # converting from a list to a Pandas Dataframe

    img_path = save_equity_plot(engine)

    with open(outpath, "w") as f:
        f.write("# Backtest Performance Report\n\n")
        f.write("## Key Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------:|\n")
        f.write(f"| Total Return | {total_return:.2%} |\n")
        f.write(f"| Sharpe Ratio | {sharpe:.2f} |\n")
        f.write(f"| Max Drawdown | {max_dd:.2%} |\n\n")

        f.write("## Equity Curve\n\n")
        f.write(f"![Equity Curve]({img_path})\n\n")

        f.write("## Periodic Returns (summary)\n\n")
        f.write(periodic_returns.describe().to_markdown() + "\n\n")


    return outpath