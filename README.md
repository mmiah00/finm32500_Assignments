# finm32500-assignment1
Our team first divided the project into several Python modules, assigning specific responsibilities to each:

## 'main.py'
This serves as the primary entry point for running backtesting simulations. It handles the entire workflow including:

Generating and loading historical market data.

Initializing the trading strategy to be tested.

Instantiating and running the ExecutionEngine.

Triggering the generation of the final performance report.

## 'engine.py '
It drives the core data processing: 

Iterating through time-series market data.

Passing market data to the strategy.

Receiving trade signals from the strategy.

Executing trades and updating portfolio state.

Simulating potential execution failures to test resilience.

## 'models.py'
This module defines the data structures used throughout the application:

/MarketDataPoint/: A dataclass representing immutable data for a single market data tick with timestamp, symbol, and price.

Order: A dataclass representing a trading order containing trade code, quantity, price, and direction (buy/sell). It includes validation functions to prevent invalid orders.

Custom Exceptions: OrderError handles specific issues during simulation processing.

strategies.py
This module contains trading logic. It features an abstract base class and concrete strategy implementations:

Strategy: Abstract base class defining the interface for all trading strategies.

Moving_average_crossover: Concrete strategy generating signals based on the crossover of short-term and long-term moving averages.

MomentumStrategy: A concrete strategy generating signals based on price momentum over a specified lookback period.



Translated with DeepL.com (free version)
