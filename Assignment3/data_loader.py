import sys
import pandas as pd 
from collections import defaultdict
from dataclasses import dataclass

df = pd.read_csv ('market_data.csv')
print(df.head() )

@dataclass(frozen=True)
class MarketDataPoint:
    def __init__ (self, timestamp, symbol, price): 
        # timestamp: datetime
        # symbol: str
        # price: float
        self.timestamp = timestamp 
        self.symbol = symbol 
        self.price = price 
    
MDPs = []  # list of market data point objects generated from market data csv 
MDPs_by_ticker = defaultdict(list)

for index, row in df.iterrows():
    try: 
        mdp = MarketDataPoint (row['timestamp'], row['symbol'], row['price'])
        MDPs.append(mdp) 
        MDPs_by_ticker[row['symbol']].append(mdp)
    except: 
        print (f"Had issues loading this row from market_data.csv:\n{row}")

# O(N) space complexity, given that you are reading in each row from the market_data.csv file and saving them as a MarketDataPoint object. 

