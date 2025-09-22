# FINM 32500 - Assignment 1
Our team first divided the project into several Python modules, assigning specific responsibilities to each:

## 'data_loader.py'
This module contains a basic method for opening any CSV document.

## 'models.py'
This module defines the data structures used throughout the application:

/MarketDataPoint/ and /Order/

We also write OrderError to handle specific issues during simulation processing.

## 'engine.py '
It drives the core data processing: 

We wrote run() to iterate through time-series market data and simulating potential execution failures.

Then, a set of criteria was designed to receive trading signals from the strategy, execute trades, and update the portfolio status. This logic is encapsulated within the `execute_order(self, order: models.Order)`


## 'strategies.py'
This module contains the logic to get a desicion of "BUY" and "SELL". 

It features an abstract base class and concrete strategy implementations:

Moving_average_crossover: Crossover of short-term and long-term moving averages.

MomentumStrategy: Price momentum over a specified lookback period.

## 'reporting.py'

This module analyzes backtesting results and generates performance reports. It is crucial because it visualizes several key financial metrics: Total Return; Sharpe Ratio and Maximum Drawdown: 

## 'main.py'
This serves as the primary entry point for running backtesting simulations. It handles the entire workflow including:

Generating and loading historical market data.

Initializing the trading strategy to be tested.

Instantiating and running the ExecutionEngine.

Triggering the generation of the final performance report.

