# finm32500-assignment1
Our team first divided the project into several Python modules, assigning specific responsibilities to each:

## 'data_loader.py'
This module contains a basic method for opening any CSV document.

## 'models.py'
This module defines the data structures used throughout the application:

/MarketDataPoint/ and /Order/

We also write OrderError to handle specific issues during simulation processing.

## 'engine.py '
It drives the core data processing: 

Iterating through time-series market data.

Passing market data to the strategy.

Receiving trade signals from the strategy.

Executing trades and updating portfolio state.

Simulating potential execution failures to test resilience.

## 'strategies.py'
This module contains the logic to get a desicion of "BUY" and "SELL". 

It features an abstract base class and concrete strategy implementations:

Moving_average_crossover: Crossover of short-term and long-term moving averages.

MomentumStrategy: Price momentum over a specified lookback period.

## 'main.py'
This serves as the primary entry point for running backtesting simulations. It handles the entire workflow including:

Generating and loading historical market data.

Initializing the trading strategy to be tested.

Instantiating and running the ExecutionEngine.

Triggering the generation of the final performance report.
