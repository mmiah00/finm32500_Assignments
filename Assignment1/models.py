# data_generator.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import random
import time
import csv

class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass
    
@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime.datetime
    symbol: str
    price: float


@dataclass
class Order:
    def __init__(self, symbol, quantity, price, status):
        self.symbol  =symbol
        self.quantity = quantity
        self.price = price
        self.status = status
    def __post_init__(self):
        if self.quantity <= 0:
            raise OrderError(f"The quantity must be positive! But receiving{self.quantity}")
        if self.side not in ["BUY", "SELL"]:
            raise OrderError(f"Invalid side: {self.side}")



