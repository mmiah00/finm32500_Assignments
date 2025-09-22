# Execution Engine
import models
import strategies
import datetime
import time
import csv
import random

class ExecutionEngine:
    def __init__(self, market_data, strategies, starting_cash):
        # Iterate through the list of MarketDataPoint objects in timestamp order.
        self.market_data = sorted(market_data, key=lambda x: x.timestamp)
        self.strategies = strategies
        self.cash = starting_cash
        self.portfolio = {}
        # simple order history for reporting
        self.order_history = []
        #In the execution engine, simulate occasional failures and raise ExecutionError; catch and log these errors to continue processing.
        self.execution_failure_chance = 0.05  #Assuming fail rate

    def run(self):
        # For each tick:
        for tick in self.market_data:
            for strategy in self.strategies:
                # Wrap order creation and execution in try/except blocks for resilience.
                try:
                    # Invoke each strategy to generate signals.
                    signals = strategy.generate_signals(tick)
                    for signal in signals:
                        # Instantiate and validate Order objects.
                        order = models.Order(signal[1],signal[2],signal[3],signal[0])

                        # Simulate failures
                        if random.random() < self.execution_failure_chance:
                            raise models.ExecutionError("Failure Occurs")
                            
                        # Execute orders by updating the portfolio dictionary.
                        self.execute_order(order)

                        # record the executed order in history for reporting
                        self.order_history.append(order)
                        
                except Exception as e:
                    print(f"Error processing tick {tick} with strategy {strategy}: {e}")
                except models.OrderError as e:
                    print(f"Invalid order with strategy {strategy}: {e}")
                except models.ExecutionError as e:
                    print(f"Execution Failure with strategy {strategy}: {e}")

    def execute_order(self, order: models.Order):
        symbol = order.symbol

        if symbol not in self.portfolio:
            self.portfolio[symbol] = {'quantity': 0, 'avg_price': 0.0}

        current_qty = self.portfolio[symbol]['quantity']
        current_avg_price = self.portfolio[symbol]['avg_price']


        if order.status == "BUY":
                new_qty = current_qty + order.quantity
                new_avg_price = ((current_avg_price * current_qty) + (order.price * order.quantity)) / new_qty

                self.portfolio[symbol]['quantity'] = new_qty
                self.portfolio[symbol]['avg_price'] = new_avg_price
                self.order_history.append(order)

        elif order.status == "SELL":
                if self.portfolio[symbol]['quantity'] == 0:
                     pass
                else:
                    new_qty = current_qty - order.quantity
                    self.portfolio[symbol]['quantity'] = new_qty
                    self.order_history.append(order)
                    if new_qty == 0:
                        self.portfolio[symbol]['avg_price'] = 0.0

        print(
            f"[{order.status}] {order.quantity} {order.symbol} @ ${order.price:.2f} | "
            f"New shares: {self.portfolio[symbol]['quantity']}, "
            f"Avg cost: ${self.portfolio[symbol]['avg_price']:.2f}"
        )
