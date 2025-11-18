from enum import Enum, auto

class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()

class Order:
    def __init__(self, symbol, qty, side, price):
        self.state = OrderState.NEW
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.price = price

    def transition(self, new_state):
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        }
        if self.state == OrderState.NEW:
            if new_state in allowed[OrderState.NEW]:
                self.state = new_state
            else:
                print('Not Allowed')
        if self.state == OrderState.ACKED:
            if new_state in allowed[OrderState.ACKED]:
                self.state = new_state
            else:
                print('Not Allowed')
        