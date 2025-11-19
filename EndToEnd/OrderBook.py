import enum
import queue
import time
from collections import defaultdict

class Order:
    def __init__(self, order_id, price, size, side, time):
        self.order_id = order_id
        self.price = price
        self.size = size
        self.side = side
        self.time = time

class Trade:
    def __init__(self, side, price, size, order_id, book_order_id):
        self.side = side
        self.price = price
        self.size = size
        self.order_id = order_id
        self.book_order_id = book_order_id

class OrderBook:
    def __init__(self):
        self.bid_prices = []
        self.bid_sizes = []
        self.ask_prices = []
        self.ask_size = []
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)
        self.open_orders = queue.Queue()
        self.trades = queue.Queue()
        self.order_id = 0

    @property
    def max_bid(self):
        if self.bids:
            return max(self.bids.keys())
        else:
            return 0
    
    @property
    def min_ask(self):
        if self.asks:
            return min(self.asks.keys())
        else:
            return float('inf')

    def add(self):
        pass

    def modify(self):
        pass

    def cancel(self):
        pass

    def process(self, order):
        if order.side == 'Buy':
            # 'Buy'
            if order.price >= self.min_ask and self.offers:
                self.process_match(order)
            else:
                self.bids[order.price].append(order)
        else:
            # 'Sell
            if order.price <= self.max_bid and self.bids:
                self.process_match(order)
            else:
                self.asks[order.price].append(order)

    def process_match(self, order):
        if order.side == 'Sell':
            levels = self.bids
        else:
            levels = self.asks
        prices = sorted(levels.keys, reverse=(order.side == 'Sell'))
        def price_check(book_price):
            if order.side == "Buy":
                return order.price < book_price
            else:
                return order.price > book_price
        for (i, price) in enumerate(prices):
            if (order.size == 0 or (price_check(price))):
                break
            order_level = levels[price]
            for (j, book_order) in enumerate(order_level):
                if order.size == 0:
                    break
                trade = self.execute(order, book_order)
                order.size = max(0, order.size - trade.size)
                book_order.size = max(0, book_order.size - trade.size)
                self.trades.put(trade)
            levels[price] = [order for order in order_level if order.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)
        if order.size > 0:
            if order.size == 'Buy':
                same_side = self.bids
                same_side[order.price].append(order)
            else:
                same_side = self.asks
                same_side[order.price].append(order)

    def execute(self, order, book_order):
        trade_size = min(order.size, book_order.size)
        return Trade(order.side, book_order.price, trade_size, order.order_id, book_order.order_id)


# self, order_id, price, size, side, time)
print('Example 1:')
ob = OrderBook()
orders = [Order(order_id=1, price = 10, side='Buy', size = 1, time = '2012-04-12'),
        Order(order_id=2, price = 10, side='Buy', size = 1, time = '2012-04-12'),
        Order(order_id=3, price = 10, side='Buy', size = 1, time = '2012-04-12')]
print('We receive these orders:')
for order in orders:
    print(order)
    ob.open_orders.put(order)
while not ob.open_orders.empty():
    ob.process(ob.open_orders.get())
print('Resulting order book:')