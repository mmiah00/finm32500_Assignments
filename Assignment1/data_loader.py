# data_generator.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import random
import time
import csv
from models import MarketDataPoint, Order


def market_data_generator(
    symbol: str,
    start_price: float,
    volatility: float = 0.01,
    interval: float = 0.1
):
    """
    Simulates a live market data feed for a given symbol using a
    Gaussian random walk.

    :param symbol: Ticker symbol (e.g., "AAPL").
    :param start_price: Initial price.
    :param volatility: Std dev of returns per tick.
    :param interval: Pause in seconds between ticks.
    :yield: MarketDataPoint(timestamp, symbol, price)
    """
    price = start_price
    while True:
        delta = random.gauss(0, volatility)
        price *= 1 + delta
        price = round(price, 2)

        yield MarketDataPoint(
            timestamp=datetime.datetime.now(),
            symbol=symbol,
            price=price
        )

        time.sleep(interval)


def generate_market_csv(
    symbol: str,
    start_price: float,
    filename: str,
    num_ticks: int = 100,
    volatility: float = 0.01,
    interval: float = 0.0
):
    """
    Generates `num_ticks` of market data and writes them to a CSV file.

    :param symbol: Ticker symbol (e.g., "AAPL").
    :param start_price: Initial price.
    :param filename: Path to output CSV.
    :param num_ticks: Number of ticks to generate.
    :param volatility: Std dev of returns per tick.
    :param interval: Pause in seconds between ticks (set to 0 for fast generation).
    """
    gen = market_data_generator(
        symbol=symbol,
        start_price=start_price,
        volatility=volatility,
        interval=interval
    )

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['timestamp', 'symbol', 'price'])

        for _ in range(num_ticks):
            tick = next(gen)
            # Write ISO-formatted timestamp for easy parsing later
            writer.writerow([tick.timestamp.isoformat(), tick.symbol, tick.price])

def read_market_data(filename: str):
    data_points = []  #list
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the head ['timestamp', 'symbol', 'price']

        for row in reader:
            timestamp = datetime.datetime.fromisoformat(row[0])  
            symbol = row[1]
            price = float(row[2]) 
            
            point = MarketDataPoint(timestamp, symbol, price)
            data_points.append(point)

    return data_points

def generate_market_csv(
    symbol: str,
    start_price: float,
    filename: str,
    num_ticks: int = 100,
    volatility: float = 0.01,
    interval: float = 0.0
):
    """
    Generates `num_ticks` of market data and writes them to a CSV file.

    :param symbol: Ticker symbol (e.g., "AAPL").
    :param start_price: Initial price.
    :param filename: Path to output CSV.
    :param num_ticks: Number of ticks to generate.
    :param volatility: Std dev of returns per tick.
    :param interval: Pause in seconds between ticks (set to 0 for fast generation).
    """
    gen = market_data_generator(
        symbol=symbol,
        start_price=start_price,
        volatility=volatility,
        interval=interval
    )

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Header
        writer.writerow(['timestamp', 'symbol', 'price'])

        for _ in range(num_ticks):
            tick = next(gen)
            # Write ISO-formatted timestamp for easy parsing later
            writer.writerow([tick.timestamp.isoformat(), tick.symbol, tick.price])

def read_market_data(filename: str):
    data_points = []  #list
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the head ['timestamp', 'symbol', 'price']

        for row in reader:
            timestamp = datetime.datetime.fromisoformat(row[0])  
            symbol = row[1]
            price = float(row[2]) 
            
            point = MarketDataPoint(timestamp, symbol, price)
            data_points.append(point)

    return data_points
