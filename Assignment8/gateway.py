# Streams price & sentiment data via TCP
import random
import socket

global MESSAGE_DELIMITER
MESSAGE_DELIMITER = "*_*"

class Gateway:
    def __init__(self,symbols=["AAPL", "MSFT", "GOOG"]):
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

    # def serialize(self, data):
    #     string = data.encode('utf-8')
    #     return string

    def serialize(self, data):
        return (json.dumps(data) + MESSAGE_DELIMITER).encode('utf-8')

    def send_message(self, data):
        # send serialized message through socket  

        message = self.serialize(data)
        dead_clients = []

        for c in self.client_sockets:
            try:
                c.sendall(message)
            except (BrokenPipeError, ConnectionResetError):
                dead_clients.append(c)

        for dc in dead_clients:
            print("[Gateway] Client disconnected.")
            self.client_sockets.remove(dc)
            dc.close()

    def deserialize(self, data):
        string = data.decode('utf-8')
        return string
    
    # def send_message(self, data):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((HOST, PORT))
    #         message = ""
    #         if "Sentiment" in data: 
    #             # sending sentiment data 
    #             message += f"{data[ticker]},{data["Score"]}" + MESSAGE_DELIMITER
    #         else: 
    #             message += f"{data[ticker]},{data["Last Price"]}" + MESSAGE_DELIMITER
    #         s.sendall(message.encode('utf-8'))  # Encode and send the message
    #         print(f"Sent: {message}")



def run_gateway():
    symbols = ["AAPL", "MSFT", "GOOG"]
    gateway = Gateway(symbols)
    
    self.establish_server()
    print("[Gateway] Waiting for clients to connect...")

    # Accept one or more clients before streaming
    self.server_socket.setblocking(False)

    tickers = ['AAPL', 'GOOG', 'MSFT']
    while True:
        # accept new connections non-blocking
        try:
            client_socket, addr = self.server_socket.accept()
            print(f"[Gateway] New client connected: {addr}")
            self.client_sockets.append(client_socket)
        except BlockingIOError:
            pass

        # broadcast data
        for ticker in tickers:
            price_data = self.market_data(ticker)
            news_data = self.market_news(ticker)

            self.send_message(price_data)
            self.send_message(news_data)

            print(f"[Gateway] Sent {ticker}: "
                    f"Price={price_data['Last Price']:.2f}, "
                    f"Sentiment={news_data['Sentiment']}")

        time.sleep(2)

gate = Gateway()
print(gate.market_data('AAPL'))