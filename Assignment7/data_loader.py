import pandas as pd 
import polars as pl
import datetime
from memory_profiler import profile


fp = "data/market_data-1.csv"

# Load the data using both pandas and polars.
pandas_df = pd.read_csv(fp)
polars_df = pl.read_csv(fp)

##########################################################################################

# Parse into a time-indexed DataFrame with columns: timestamp, symbol, price.
pandas_df['timestamp'] = pd.to_datetime(pandas_df['timestamp'])
polars_df = polars_df.with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S")
)
pandas_df = pandas_df.set_index('timestamp')

##########################################################################################

# Demonstrate equivalent parsing logic in both libraries.

# 1. Check Datatypes of Each Column 
print(pandas_df.dtypes)
print() 
print(polars_df.dtypes)

# 2. Check first few rows of the dataframe 
print(pandas_df.head())
print() 
print(polars_df.head())

##########################################################################################

# Compare ingestion time and memory usage using profiling tools
# We are using the memory profiler library to find ingestion time and memory usage. 
# To run, type in the command line: python3 -m memory_profiler data_loader.py


@profile
def load_pandas():
    print ("---Checking ingestion time and memory usage of Pandas---")
    pd.read_csv(fp)

@profile
def load_polars():
    print ("---Checking ingestion time and memory usage of Polars---")
    pl.read_csv(fp)

load_pandas() 
load_polars() 

