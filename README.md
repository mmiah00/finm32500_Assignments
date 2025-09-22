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
