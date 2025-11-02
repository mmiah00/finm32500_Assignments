import pandas as pd
import polars as pl
import json
import multiprocessing
import concurrent.futures
from memory_profiler import profile
from data_loader import polars_df, pandas_df
from portfolio_agg import * 
import matplotlib.pyplot as plt
import time


# filtered_df_pandas = calc_metrics_seq_pandas(pandas_df, "AAPL")
# filtered_df_polars = calc_metrics_seq_polars(polars_df, "AAPL")
if __name__ == '__main__':
    starttime1 = time.time()
    processing_pandas()
    endtime1 = time.time()
    starttime2 = time.time()
    processing_polars()
    endtime2 = time.time()
    filtered_df_pandas.to_json('part4_pandas.json') 
    filtered_df_polars.write_json('part4_polars.json')
    elapsed_time1 = (endtime1-starttime1)
    elapsed_time2 = (endtime2-starttime2)
    plt.bar(["pandas", "polars"], [elapsed_time1, elapsed_time2])
    plt.show()

# Each of these tools serve a function in a particular space. Polars lends itself well to
# scale and larger data given the inherent consideration of big data tasks. However, for
# smaller scale projects tools such as pandas seem to be sufficient or better suited. 



