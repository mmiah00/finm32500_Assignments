import sqlite3 as sql
from data_loader import DataLoader

con = sql.connect('market_data.db')

cur = con.cursor()

# cur.execute("""CREATE TABLE tickers (
#     ticker_id INTEGER PRIMARY KEY,
#     symbol TEXT NOT NULL UNIQUE,
#     name TEXT,
#     exchange TEXT
# );""")

# cur.execute("""CREATE TABLE prices (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     timestamp TEXT NOT NULL,
#     ticker_id INTEGER NOT NULL,
#     open REAL,
#     high REAL,
#     low REAL,
#     close REAL,
#     volume INTEGER,
#     FOREIGN KEY (ticker_id) REFERENCES tickers(ticker_id)
# );
# """)

# data = DataLoader('market_data_multi.csv','tickers.csv')

# data.market_data.to_sql('prices', con, if_exists='append', index=False)
# data.tickers.to_sql('tickers', con, if_exists='append', index=False)

# retrieve = cur.execute("SELECT * FROM prices WHERE ticker = 'AAPL'")
# print(retrieve.fetchall())

# retrieve = cur.execute(
# """
# SELECT *
# FROM prices
# WHERE ticker = 'AAPL' AND timestamp BETWEEN '2025-11-18' AND '2025-11-20';
# """)
# print(retrieve.fetchall())

# average = cur.execute(
# """
# SELECT ticker, DATE(timestamp) AS day, avg(close)
# FROM prices
# GROUP BY ticker, day

# """
# )
# print(average.fetchall())

# returns = cur.execute(
# """
# WITH WeeklyPrices AS (
#     SELECT
#         ticker,
#         MAX(CASE WHEN timestamp = '2025-11-17 09:30:00' THEN close END) AS start_price,
#         MAX(CASE WHEN timestamp = '2025-11-21 16:00:00' THEN close END) AS end_price
#     FROM prices
#     WHERE timestamp IN ('2025-11-17 09:30:00', '2025-11-21 16:00:00')
#     GROUP BY ticker
# )
# SELECT
#     ticker,
#     ROUND(((end_price - start_price) * 100 / start_price), 2) AS return
# FROM WeeklyPrices
# ORDER BY return DESC
# LIMIT 3;
# """)
# print(returns.fetchall())

# firstlast = cur.execute(
# """
# SELECT
# ticker, 
# MAX(CASE WHEN timestamp = '2025-11-17 09:30:00' THEN close END) AS day1start,
# MAX(CASE WHEN timestamp = '2025-11-17 16:00:00' THEN close END) AS day1end,
# MAX(CASE WHEN timestamp = '2025-11-18 09:30:00' THEN close END) AS day2start,
# MAX(CASE WHEN timestamp = '2025-11-18 16:00:00' THEN close END) AS day2end,
# MAX(CASE WHEN timestamp = '2025-11-19 09:30:00' THEN close END) AS day3start,
# MAX(CASE WHEN timestamp = '2025-11-19 16:00:00' THEN close END) AS day3end,
# MAX(CASE WHEN timestamp = '2025-11-20 09:30:00' THEN close END) AS day4start,
# MAX(CASE WHEN timestamp = '2025-11-20 16:00:00' THEN close END) AS day4end,
# MAX(CASE WHEN timestamp = '2025-11-21 09:30:00' THEN close END) AS day5start,
# MAX(CASE WHEN timestamp = '2025-11-21 16:00:00' THEN close END) AS day5end
# FROM prices
# GROUP BY ticker
# """
# )
# print(firstlast.fetchall())
