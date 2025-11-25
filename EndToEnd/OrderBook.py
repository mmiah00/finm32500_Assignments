import enum
# import queue
from queue import PriorityQueue
import time
from collections import defaultdict

class Order:
    def __init__(self, order_id, price, size, side, time):
        self.order_id = order_id
        self.price = price
        self.size = size
        self.side = side
        self.time = time
        self.status = None 

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
        self.open_orders = PriorityQueue() #queue.Queue()
        self.trades = PriorityQueue() # queue.Queue()
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

    def add(self, order):
        order.status = "Added"
        self.open_orders.put((order.price, order.time,order.order_id, order))
        print(f"Order {order.order_id} added to book.") 
        return order 

    def modify(self, old_order, new_price=None, new_size=None, new_side=None):
        order.status = "Modified"
        if new_price: 
            old_order.price = new_price
        if new_size:
            old_order.size = new_size
        if new_side:
            old_order.side = new_side
        self.cancel(old_order)
        self.open_orders.put((old_order.price, old_order.time,old_order.order_id, old_order))
        return old_order

    def cancel(self, order):
        order.status = "Canceled" 

        new_orders = PriorityQueue()
        while not self.open_orders.empty():
            current_order = self.open_orders.get()[-1]
            if current_order.order_id != order.order_id:
                new_orders.put((current_order.price, current_order.time,current_order.order_id,current_order))
        self.open_orders = new_orders
        print(f"Order {order.order_id} canceled from book.")
        return order 

    def process(self, order):
        if order.side == 'Buy':
            # 'Buy'
            if order.price >= self.min_ask and self.asks:
                self.process_match(order)
            else:
                self.bids[order.price].append(order)
        elif order.side == 'Sell':
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
        # prices = sorted(levels.keys, reverse=(order.side == 'Sell'))
        prices = sorted(levels, reverse=(order.side == 'Sell'))
        def price_check(book_price):
            if order.side == "Buy":
                return order.price < book_price
            else:
                return order.price > book_price
        for (i, price) in enumerate(prices):
            if (order.size == 0 or (price_check(price))):
                break
            order_level = levels[price]
            # priority = 1 # lower priority val, gets executed first 
            for (j, book_order) in enumerate(order_level):
                if order.size == 0:
                    break
                trade = self.execute(order, book_order)
                print(order.size, book_order.size, trade.size)
                order.size = max(0, order.size - trade.size)
                book_order.size = max(0, book_order.size - trade.size)
                # self.trades.put(trade)
                self.trades.put((order.price, order.time, order.order_id, id(trade), trade))
                # priority += 1
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


# # self, order_id, price, size, side, time)
# print('Example 1:')
# ob = OrderBook()
# orders = [Order(order_id=1, price = 10, side='Buy', size = 1, time = '2012-04-12'),
#         Order(order_id=2, price = 10, side='Buy', size = 1, time = '2012-04-12'),
#         Order(order_id=3, price = 10, side='Buy', size = 1, time = '2012-04-12')]
# print('We receive these orders:')
# # priority = 1 # lower priority val, gets executed first 
# for order in orders:
#     print(order)
#     # ob.open_orders.put(order)
#     ob.open_orders.put((order.price, order.time,order.order_id,order))
#     # priority += 1
# print('Processing orders...')
# while not ob.open_orders.empty():
#     ob.process(ob.open_orders.get()[-1])
# print('Resulting order book:')