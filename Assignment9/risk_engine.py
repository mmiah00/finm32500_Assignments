class RiskEngine:
    def __init__(self, max_order_size=1000, max_position=2000):
        self.max_order_size = max_order_size
        self.max_position = max_position
        self.check_condition = True

    def check(self, order) -> bool:
        self.check_condition = True
        if order.qty > self.max_order_size:
            print('Nope order size too large')
            self.check_condition = False
        if (float(order.qty) * float(order.price)) > self.max_position:
            print('Nope, position too large')
            self.check_condition = False
        return self.check_condition
    def update_position(self, order):
        self.check_condition = self.check(order)
        if self.check_condition is True:
            self.position += self.qty

