# Streams price & sentiment data via TCP
import random
import socket

class Gateway:
    def __init__(self):
        pass

    def market_data(self, ticker):
        starting_price = random.uniform(10,1000)
        

        bids = []
        asks = []

        for i in range(10):
            bid = starting_price - (starting_price * 0.001) - (i * 0.1)
            ask = bid = starting_price + (starting_price * 0.001) + (i * 0.1)
            size = random.uniform(5,100)
            bids.append([bid, size])
            asks.append([ask, size])

        market_data = {'Ticker': ticker, 'Bids':bids, 'Asks': asks, 'Last Price': starting_price, 'Volume': random.randint(100,10000)}

        return market_data
    
    def market_news(self, ticker):
        score = random.randint(0,100)
        if score < 50:
            sentiment = "negative"
        elif score == 50:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        sentiment_data = {'Ticker': ticker, 'Sentiment': sentiment, 'Score': score}

        return sentiment_data
    
    def establish_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def serialize(self, data):
        string = data.encode('utf-8')
        return string

    def deserialize(self, data):
        string = data.decode('utf-8')
        return string
    
gate = Gateway()
print(gate.market_data('AAPL'))