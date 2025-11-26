Compare:
File size: The market_data.csv file is much larger than the db file which contains both prices and tickers. The parquet file will usually be smaller than the SQL file due to the way the data is compressed.

Query speed (for at least two representative queries): SQL is going to be much faster for lookups than parquet. However, parquet takes over when you begin to increase the complexity of the ask. Aggregration queries really show Parquet as being more efficient than SQL.

Ease of integration with analytics workflows: Each of them is relatively easy to implement. The bigger hurdle would likely be familiarizing with SQL, although this language isn't too challenging to work with.

Discuss:
When to use SQLite3 vs Parquet in trading systems. SQL would be a great addition to trading systems given the fast insertion or lookup into the database. Parquet would be better in backtesting scenarios.

How each format supports backtesting, live trading, and research. The formats have pros and cons for each. In the case of SQL, the database form is much less efficient for backtesting or research but better in live scenarios. Whereas, parquet is the opposite. 
