import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit

api = tradeapi.REST(key_id='PKS3ESRPJZHGHE3FY4BYP77JI6', secret_key='A3JoYsEQ3sPJcFRHDQfSQgv5zepQPE7Muaapz9c4NRYa',base_url='https://paper-api.alpaca.markets', api_version='v2')

# api = REST()

df = api.get_bars("AAPL", TimeFrame(45, TimeFrameUnit.Minute), "2021-06-08", "2021-06-08", adjustment='raw').df

print(df)