import time
from datetime import datetime, date, time as dtime
from zoneinfo import ZoneInfo  

from PriceLoader import PriceLoader
from DataCleaner import Cleaner
from Momentum import Momentum
from Gateway import Gateway
import pandas as pd
import os


MARKET_TZ = ZoneInfo("America/New_York")

# Market hours (local to MARKET_TZ)
MARKET_OPEN  = dtime(9, 30)   # 9:30 AM
MARKET_CLOSE = dtime(16, 0)   # 4:00 PM

# Date range this will run (12-01-2025 to 12-05-2025) 
START_DATE = date(2025, 12, 1)    
END_DATE   = date(2025, 12, 5)    


def do_work():
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
    ticker = 'AAPL'

    gate = Gateway(df, ticker)
    market_data = gate.stream_data()
    print(market_data)
    print(f"[{datetime.now(MARKET_TZ)}] Running trading task...")


# ---- MAIN LOOP ----
base = '/Users/ericbeechen/Documents/GitHub/finm32500_Assignments/EndToEnd/'
directory = f'{base}data/'

while True:
    now = datetime.now(MARKET_TZ)
    today = now.date()
    current_time = now.time()
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    # Stop completely after the end date
    if today > END_DATE:
        print("End date passed. Exiting script.")
        break

    # Check if we are within the desired date range
    in_date_range = START_DATE <= today <= END_DATE

    # Check if it's a weekday (Mon–Fri)
    is_weekday = weekday < 5

    # Check if we're within market hours
    in_market_hours = MARKET_OPEN <= current_time <= MARKET_CLOSE

    if in_date_range and is_weekday and in_market_hours:
        do_work()
    else:
        # do nothing out of market hours 
        pass

    time.sleep(10)   # sleep for 10 seconds before loop restarts 
