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
                        order = models.Order(*signal)

                        # Simulate failures
                        if random.random() < self.execution_failure_chance:
                            raise models.ExecutionError("Failure Occurs")
                            
                        # Execute orders by updating the portfolio dictionary.
                        self.execute_order(order)
                except Exception as e:
                    print(f"Error processing tick {tick} with strategy {strategy}: {e}")
                except models.OrderError as e:
                    print(f"Invalid order with strategy {strategy}: {e}")
                except models.ExecutionError as e:
                    print(f"Execution Failure with strategy {strategy}: {e}")

    def execute_order(self, order):
        if order.symbol not in self.portfolio:
            self.portfolio[order.symbol] = 0

        if order.side == "BUY":
            self.portfolio[order.symbol] += order.quantity * order.price
            self.cash -= order.quantity * order.price
        elif order.side == "SELL":
            self.portfolio[order.symbol] -= order.quantity * order.price
            self.cash += order.quantity * order.price

        print(f"Executed {order.side} order for {order.quantity} of {order.symbol} at {order.price}. Current position: {self.portfolio[order.symbol]}")
