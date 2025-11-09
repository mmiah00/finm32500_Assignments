# Receives prices and maintains shared memory
import socket
import time

class OrderBook:

    def __init__(self):
        self.orderbook = {}
        self.gateway_host = "127.0.0.1"
        self.gateway_port = 9000

    def receive(self, data):
        ticker = data['Ticker']
        bids = [(bid, size) for bid, size in data['Bids']]
        asks = [(ask, size) for ask, size in data['Asks']]
        self.orderbook[ticker] = {
            'Bids': bids,
            'Asks': asks,
            'Volume': data.get('Volume', 0)
        }

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



orders = OrderBook()
# print(orders.orderbook)
# orders.receive({
#     "Ticker": "AAPL",
#     'Bids': [[566.998999508781, 64.55952794748748], [567.098999508781, 48.60449553409992], [567.1989995087811, 7.04372806661727], [567.298999508781, 85.36519427143816], [567.398999508781, 5.587452624670333], [567.498999508781, 12.757498948284272], [567.598999508781, 30.815752676886056], [567.6989995087811, 12.601266364394844], [567.798999508781, 75.79354653426816], [567.898999508781, 42.147903895082635]],
#     'Asks': [[566.998999508781, 64.55952794748748], [567.098999508781, 48.60449553409992], [567.1989995087811, 7.04372806661727], [567.298999508781, 85.36519427143816], [567.398999508781, 5.587452624670333], [567.498999508781, 12.757498948284272], [567.598999508781, 30.815752676886056], [567.6989995087811, 12.601266364394844], [567.798999508781, 75.79354653426816], [567.898999508781, 42.147903895082635]], 
#     'Volume': 1971
#     })
# print(orders.orderbook)
