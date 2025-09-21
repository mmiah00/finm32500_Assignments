# data_generator.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import random
import time
import csv

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime.datetime
    symbol: str
    price: float


class Order:
    def __init__(self, symbol, quantity, price, status):
        self.symbol  =symbol
        self.quantity = quantity
        self.price = price
        self.status = status

class TradingContainer:
    def __init__(self):
        self.market_data_buffer = []  # list of MarketDataPoint

        self.positions = {}

        self.signals = []

    def buffer_market_data(self, tick: MarketDataPoint):
        self.market_data_buffer.append(tick)

    def add_signal(self, action: str, symbol: str, qty: int, price: float):
        self.signals.append((action, symbol, qty, price))

class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass
