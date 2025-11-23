import alpaca_trade_api as tradeapi

api = tradeapi.REST('PKS3ESRPJZHGHE3FY4BYP77JI6', 'A3JoYsEQ3sPJcFRHDQfSQgv5zepQPE7Muaapz9c4NRYa', 'https://paper-api.alpaca.markets/v2')

data = api.get_barset('AAPL', '1Min', limit=1).df['AAPL']