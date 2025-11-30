import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from dotenv import load_dotenv
import os

load_dotenv()

api = tradeapi.REST(key_id=os.getenv('KEY_ID'), secret_key=os.getenv('SECRET_KEY'),base_url='https://paper-api.alpaca.markets', api_version='v2')

df = api.get_bars("AAPL", TimeFrame(45, TimeFrameUnit.Minute), "2021-06-08", "2021-06-08", adjustment='raw').df

print(df)