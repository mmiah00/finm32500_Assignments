
def find_total_return (self, marketdatapoints): 
    total  = 0 

    prev_order = marketdatapoints[0] # FILL IN WITH REAL LIST NAME 

    for i in range (1, len(marketdatapoints)): 
        curr_order = marketdatapoints[i] 
        simple_return = (curr_order.price - prev_order.price - 0.0) / prev_order.price
        total += simple_return 

        prev_order = curr_order 

    return total  


def periodic_returns(self, marketdatapoints): 
    # periodic return = ((end_val / beg_val) - 1) * 100% 

    periodic_returns = [] 

    prev_order = marketdatapoints[0] 

    for i in range (1, len(marketdatapoints)): # FILL IN WITH REAL NAME 
        curr_order = marketdatapoints[i] 

        calc = ((curr_order.price / prev_order.price) - 1) # * 100 if i want to find the percentage, otherwise leave between 0-1 
        periodic_returns.append(calc) 
        
        prev_order = curr_order

    return periodic_returns  

def calc_sharpe_ratio(self, marketdatapoints, periodic_returns): 
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
    


def max_drawdown (self, marketdatapoints): 
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


# An equity-curve plot visually represents an investment's or trading strategy's 
# performance over time, with the y-axis showing the account value and the x-axis 
# representing time or trade number.