import sys
import pandas as pd 
from collections import defaultdict
from dataclasses import dataclass

df = pd.read_csv ('market_data.csv')


@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: str
    symbol: str
    price: float
    
MDPs = []  # list of market data point objects generated from market data csv 
# MDPs_by_ticker = defaultdict(list)

for index, row in df.iterrows():
    try: 
        mdp = MarketDataPoint (row['timestamp'], row['symbol'], row['price'])
        MDPs.append(mdp) 
        # print(f"Added mdp. Timestamp : {row['timestamp']} | Symbol : {row['symbol']} | Price : {row['price']}")
        # MDPs_by_ticker[row['symbol']].append(mdp)
    except Exception as e: 
        print(e)
        print (f"Had issues loading this row from market_data.csv:\n{row}\n")

# O(N) space complexity, given that you are reading in each row from the market_data.csv file and saving them as a MarketDataPoint object. 

