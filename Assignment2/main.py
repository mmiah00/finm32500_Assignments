from PriceLoader import PriceLoader
from BenchmarkStrategy import BenchmarkStrategy
from MovingAverageStrategy import MovingAverageStrategy
from VolatilityBreakoutStrategy import VolatilityBreakoutStrategy
from MACDStrategy import MACDStrategy
from RSIStrategy import RSIStrategy

"""
Get all price data using PriceLoader 
"""
loader = PriceLoader()
ticks = loader.load_tickers() 
# loader.download_ticker_prices()  
price_data = loader.get_select_ticker_data(loader.tickers)

# TO PEEK AT DATA
#
# for ticker in price_data: 
#     print(f"== Data for ticker: {ticker} ==")
#     ticker_data = price_data[ticker]
#     print(ticker_data.head())
#     print("===========")


print("Finished loading.")
print() 

"""
Run Strategies Using Price Data
"""

# print ("Testing Benchmark Strategy")
strat1 = BenchmarkStrategy() 
strat1.run(price_data)
benchmark_results = strat1.get_results() 
benchmark_results.to_csv('results/benchmark_results.csv')
# print("Results from Benchmark Strategy")
# print() 
# print(benchmark_results.head())

##########################################################################

# print ("Testing Moving Average Strategy")
strat2 = MovingAverageStrategy()
strat2.run(price_data)

ma_results = strat2.get_results()
ma_results.to_csv('results/ma_results.csv')

# print(ma_results.tail())

##########################################################################

# print("Testing Volatility Breakout Strategy")
# strat3 = VolatilityBreakoutStrategy()
# strat3.run(price_data)

# vbs_results = strat3.get_results()
# vbs_results.to_csv('results/vbs_results.csv')

# print(vbs_results.tail())

##########################################################################

# print ("Testing MACD Strategy")
strat4 = MACDStrategy()
strat4.run(price_data)

macd_results = strat4.get_results()
macd_results.to_csv('results/macd_results.csv')

# print(macd_results.tail())

##########################################################################

# print("Testing RSI Strategy")
strat5 = RSIStrategy()
strat5.run(price_data)

rsi_results = strat5.get_results()
rsi_results.to_csv('results/rsi_results.csv')

# print(rsi_results.tail())

