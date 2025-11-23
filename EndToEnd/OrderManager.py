'''
📤 Step 3: Order Manager & Gateway
Objective: Validate and record orders before execution.

Requirements:

OrderManager - Implement checks for capital sufficiency and risk limits.
Capital sufficiency should check if enough capital exists to execute the order.
Risk limits should check orders per minute and if executing the order would exceed total buy or total sell position limits.
'''

class OrderManager: 

    def __init__(self, initial_capital=100000, max_orders_per_minute=60, max_position_size=300):
        self.initial_capital = initial_capital
        self.available_capital = initial_capital
        self.max_orders_per_minute = max_orders_per_minute
        self.max_position_size = max_position_size
        self.orders_executed = []
        self.current_minute = None
        self.orders_in_current_minute = 0
        self.current_position = 0

    def validate_order(self, order):
        # Check capital sufficiency
        required_capital = order.price * order.size
        if order.side == 'Buy' and required_capital > self.available_capital:
            return False, "Insufficient capital"

        # Check risk limits
        if self.current_minute != order.time.minute:
            self.current_minute = order.time.minute
            self.orders_in_current_minute = 0

        if self.orders_in_current_minute >= self.max_orders_per_minute:
            return False, "Exceeded orders per minute limit"

        projected_position = self.current_position + (order.size if order.side == 'Buy' else -order.size)
        if abs(projected_position) > self.max_position_size:
            return False, "Exceeded position size limit"

        return True, "Order is valid"

    def record_order(self, order):
        is_valid, message = self.validate_order(order)
        if is_valid:
            self.orders_executed.append(order)
            self.orders_in_current_minute += 1
            if order.side == 'Buy':
                self.available_capital -= order.price * order.size
                self.current_position += order.size
            else:
                self.available_capital += order.price * order.size
                self.current_position -= order.size
        return is_valid, message