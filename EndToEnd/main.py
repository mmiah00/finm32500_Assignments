from PriceLoader import PriceLoader
from DataCleaner import Cleaner
import os

"""
Get all price data using PriceLoader 
"""
# print(os.getcwd())
loader = PriceLoader()
ticks = loader.load_tickers() 
# loader.download_ticker_prices()  
loader.get_select_ticker_data(loader.tickers)
directory = '/Users/ericbeechen/Documents/GitHub/finm32500_Assignments/EndToEnd/data/'
names = []
for entry in os.scandir(directory):
    names.append(entry.name)
for name in names:
    cleaner = Cleaner(name)

