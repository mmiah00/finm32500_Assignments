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
        self.__short_windows = short_window
        self.__long_windows = long_window
        self.__quantity = quantity
        self.__prices=[]
        self.__short_ma = 0
        self.__long_ma = 0
        
    def generate_signals(self, tick):  #tick: MarketDataPoint
        self.__prices.append(tick.price)
        if len(self.__prices) < self._long_window:
            return []
        
        short_ma = sum(self.__prices[-self.__short_window:]) / self.__short_window
        long_ma = sum(self.__prices[-self.__long_window:]) / self.__long_window

        if short_ma > long_ma:
            return [("BUY", tick.symbol, self.__quantity, tick.price)]
        elif short_ma < long_ma:
            return [("SELL", tick.symbol, self.__quantity, tick.price)]
        else:
            return []

class MomentumStrategy(Strategy):
    def __init__(self, lookback=3, quantity=10):
        self.__lookback = lookback
        self.__quantity = quantity
        self.__prices = []

    def generate_signals(self, tick: MarketDataPoint):
        self._prices.append(tick.price)
        if len(self.__prices) <= self.__lookback:
            return []

        momentum = tick.price - self.__prices[-self.__lookback]

        if momentum > 0:
            return [("BUY", tick.symbol, self.__quantity, tick.price)]
        elif momentum < 0:
            return [("SELL", tick.symbol, self.__quantity, tick.price)]
        else:
            return []
