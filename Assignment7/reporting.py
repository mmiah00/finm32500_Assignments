import pandas as pd
import json
import multiprocessing
import concurrent.futures
from memory_profiler import profile
from data_loader import polars_df, pandas_df
from portfolio_agg import * 


# filtered_df_pandas = calc_metrics_seq_pandas(pandas_df, "AAPL")
# filtered_df_polars = calc_metrics_seq_polars(polars_df, "AAPL")
if __name__ == '__main__':
    processing_pandas()
    processing_polars()
    filtered_df_pandas.to_json('part4_pandas.json') 
    filtered_df_polars.to_json('part4_polars.json')
