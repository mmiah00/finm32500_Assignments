import multiprocessing
import concurrent.futures


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

@profiler 
def threading_ex(): 
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(calc_rolling_sharpe_pd, 5)
        result.append(executor.map(calc_rolling_sharpe_pd, result))

    for r in result:
        print(r)

@profiler 
def processing_ex(): 
    result2 = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        executor.submit(calc_rolling_sharpe_pd, 5)
        result.append(executor.map(calc_rolling_sharpe_pd, result2))

    for r in result2:
        print(r)
