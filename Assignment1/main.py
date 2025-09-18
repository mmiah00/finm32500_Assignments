# data_generator.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import random
import time
import csv
from models import MarketDataPoint, Order
from data_loader import market_data_generator,generate_market_csv, read_market_data, generate_market_csv,read_market_data
def unit_test():
    order = Order("AAPL", 10, 150.0, "buy") #mutable
    point = MarketDataPoint(datetime.datetime.now(), "AAPL", 150.0) #frozen dataclass，immutable

    try:
        order.price = 100.0   
        print(f"Successful update: order.price = {order.price}")
    except Exception as e:
        print(f"Unsuccessful update:", e)

    try:
        point.price = 100.0     
        print(f"Successful update: point.quantity = {point.price}")
    except Exception as e:
        print("Unsuccessful update:", e)


if __name__ == "__main__":
    # Example: generate 500 ticks for AAPL starting at $150.00 into a file
    generate_market_csv(
        symbol="AAPL",
        start_price=150.0,
        filename="market_data.csv",
        num_ticks=500,
        volatility=0.02,
        interval=0.01
    )
    print("market_data.csv generated with 500 ticks.")

    points = read_market_data("market_data.csv")  #Buffer incoming MarketDataPoint instances in a list

    unit_test() #Demonstrate in a unit test that you can update Order.status but not MarketDataPoint.price