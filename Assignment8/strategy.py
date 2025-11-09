# Generates trading signals and sends orders
import socket
from collections import defaultdict

class Strategy:
    def __init__(self):
        self.gateway_host = "127.0.0.1"
        self.gateway_port = 9000
        self.order_host = "127.0.0.1"
        self.order_port = 9100
        self.sentiment_scores = defaultdict(float)
        self.last_prices = {}


    def connect(self):
        for i in range(3):
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((self.gateway_host, self.gateway_port))
                return server_socket
            except:
                if i < 2:
                    time.sleep(1.0)
                else:
                    raise RuntimeError(f"Oops")
                
    def connect_order(self):
        for i in range(3):
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((self.order_host, self.order_port))
                return server_socket
            except:
                if i < 2:
                    time.sleep(1.0)
                else:
                    raise RuntimeError(f"Oops")
                
    def process_market(self, data):
        ticker = data["Ticker"]
        price = data.get('Last Price', 0)
        last_price = self.last_prices["Ticker"]
        if ticker not in self.last_prices:
            signal = None
        if price > last_price and self.sentiment_scores.get(ticker, 0) > 50:
            signal = 'Buy'
        elif price < last_price and self.sentiment_scores.get(ticker, 0) < 50:
            signal = 'Sell'
        else:
            signal = None
        if signal is not None:
            signal = {
                'Ticker': ticker, 
                'Action': signal,
                'Price': price,
            }
        return signal
    
    def create_order(self, signal):
        order = {
            'Symbol': signal['Ticker'],
            'Side': signal['Action'],
            'Price': signal['Price']
        }
        return order

    def process_news(self, data):
        ticker = data["Ticker"]
        score = data['Score']
        self.sentiment_scores[ticker] = score