from PriceLoader import PriceLoader
from DataCleaner import Cleaner
from Momentum import Momentum
import pandas as pd
import os


# print(os.getcwd())
# loader = PriceLoader()
# ticks = loader.load_tickers() 
# loader.download_ticker_prices()  
# loader.get_select_ticker_data(loader.tickers)
base = '/Users/ericbeechen/Documents/GitHub/finm32500_Assignments/EndToEnd/'
directory = f'{base}data/'
names = []
tickers = []
for entry in os.scandir(directory):
    names.append(entry.name)
    tickers.append(entry.name.split('.')[0].split('_')[0])
# for name in names:
#     cleaner = Cleaner(name)

df = pd.read_csv(f'{base}cleaned/{tickers[0]}_7d.csv')
momentum = Momentum(df)
results = momentum.run()
print(results)

