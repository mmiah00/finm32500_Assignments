import multiprocessing
import concurrent.futures
from memory_profiler import profile

def calc_MA_pd (symbol, df):
    # calculates 20-period moving average per symbol 
    df["Moving_MA"] = df[symbol].rolling(window=20).mean()

    return df 

def calc_rolling_std_pd (symbol, df, window=20):
    # calculates 20-period moving average per symbol 
    df["Rolling Std"] = df[symbol].rolling(window=20).std()

    return df 

def calc_rolling_sharpe_pd (symbol, df, window=20): 
    df["Rolling Sharpe"] = df['Moving_MA']/df['Rolling Std']
    return df

##########################################################################################

# Computing metrics using pandas(pd) 

def calc_MA_pl (symbol, df):
    # calculates 20-period moving average per symbol 
    new_df = df.with_columns(
        df[symbol].rolling_mean(window_size=window).alias("ma_20")
    )

    return new_df 

def calc_rolling_std_pl (symbol, df, window=20):
    # calculates 20-period moving average per symbol 
    new_df = df.with_columns(
        df[symbol].rolling_std(window_size=window).alias("std_20")
    )

    return new_df 

def calc_rolling_sharpe_pl (symbol, df, window=20): 
    new_df = df.with_columns(
        (df["rolling_mean"] / df["rolling_std"]).alias("rolling_sharpe")
    )
    return new_df

##########################################################################################


@profile
def threading_ex(): 
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(calc_rolling_sharpe_pd, 5)
        result.append(executor.map(calc_rolling_sharpe_pd, result))

    for r in result:
        print(r)

@profile
def processing_ex(): 
    result2 = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        executor.submit(calc_rolling_sharpe_pd, 5)
        result2.append(executor.map(calc_rolling_sharpe_pd, result2))

    for r in result2:
        print(r)

print("Testing threading on rolling sharpe calculation.")
threading_ex() 

print("Testing multiprocessing on rolling sharpe calculation.")
processing_ex() 

# Discuss GIL limitations and when multiprocessing is preferred.
# Determining when to use multithreading vs. multiprocessing often comes down to the nature of the tasks we're solving. In the case of
# multithreading, we need to be cautious of the GIL. This simplifies memory management but limits python usage to one thread. 
# Part of the advantage to multithreading is more seamless communication between memory. To use multiprocessing we bypass this GIL
# constraint and allow more independent process to run. This however makes memory communication more difficult.