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
