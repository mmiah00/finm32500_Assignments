# data_generator.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import random
import time
import csv
from models import MarketDataPoint, Order

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick):  #tick: MarketDataPoint
        pass


class Moving_average_crossover(Strategy):
    def __init__(self, short_window=3, long_window=5, quantity=10):
        self.short_windows = short_window
        self.long_windows = long_window
        self.quantity = quantity
        self.prices=[]
        self.short_ma = 0
        self.long_ma = 0
        
    def generate_signals(self, tick):  #tick: MarketDataPoint
        self.prices.append(tick.price)
        if len(self.prices) < self.long_windows:
            return []
        
        short_ma = sum(self.prices[-self.short_windows:]) / self.short_windows
        long_ma = sum(self.prices[-self.long_windows:]) / self.long_windows

        if short_ma > long_ma:
            return [("BUY", tick.symbol, self.quantity, tick.price)]
        elif short_ma < long_ma:
            return [("SELL", tick.symbol, self.quantity, tick.price)]
        else:
            return []

class MomentumStrategy(Strategy):
    def __init__(self, lookback=3, quantity=10):
        self.lookback = lookback
        self.quantity = quantity
        self.prices = []

    def generate_signals(self, tick: MarketDataPoint):
        self.prices.append(tick.price)
        if len(self.prices) <= self.lookback:
            return []

        momentum = tick.price - self.prices[-self.lookback]

        if momentum > 0:
            return [("BUY", tick.symbol, self.quantity, tick.price)]
        elif momentum < 0:
            return [("SELL", tick.symbol, self.quantity, tick.price)]
        else:
            return []
