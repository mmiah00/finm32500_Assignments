import pandas as pd
import json
import multiprocessing
import concurrent.futures
from memory_profiler import profile
from data_loader import polars_df, pandas_df
import portfolio_agg 

if __name__ == '__main__':
    
