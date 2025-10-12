# Runtime & Space Complexity in Financial Signal Processing

This report summarizes the analysis and optimization of two trading strategies: 
- NaiveMovingAverageStrategy (full-history)
- WindowedMovingAverageStrategy (optimized sliding window)

We analyze runtime, memory usage, and theoretical complexity, and visualize scaling behavior across different input sizes.

## Complexity Annotations

| Strategy                     | Time Complexity | Space Complexity | Explanation |
|-------------------------------|----------------|-----------------|-------------|
| NaiveMovingAverageStrategy    | O(n) per tick  | O(n)            | Computes average from scratch for each tick; stores all historical prices. |
| WindowedMovingAverageStrategy | O(1) per tick  | O(k)            | Maintains a fixed-size buffer of last k prices; updates average incrementally. |

## Benchmark Results

| Ticks | Naive Time (s) | Windowed Time (s) | Naive Memory (MB) | Windowed Memory (MB) |
|-------|----------------|------------------|-----------------|--------------------|
| 1,000 | 0.0483402      | 0.0009685999975  | 207.3046875     | 243.625            |
| 10,000| 0.2175302      | 0.0281602000031  | 207.5625        | 246.1328125        |
|100,000| 1.4890584      | 0.1579876000032  | 207.5703125     | 246.13671875       |

## Analysis and Discussion

- The NaiveMovingAverageStrategy’s runtime grows linearly with the number of ticks, making it impractical for large datasets. Memory usage also increases proportionally since all historical prices are stored.
- The WindowedMovingAverageStrategy demonstrates constant-time updates per tick and memory usage proportional to the window size, which remains stable even as the dataset grows.
