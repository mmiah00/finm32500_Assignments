import time
from datetime import datetime, date, time as dtime
from zoneinfo import ZoneInfo  

from AlpacaDataFetcher import AlpacaDataFetcher
from Momentum import Momentum
from Gateway import Gateway
import pandas as pd
import os
from pathlib import Path
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
from types import SimpleNamespace

load_dotenv()

# Dry-run mode: set DRY_RUN=true in your environment to avoid placing real orders
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() in ('1', 'true', 'yes')


MARKET_TZ = ZoneInfo("America/New_York")

# Market hours (local to MARKET_TZ)
MARKET_OPEN  = dtime(9, 30)   # 9:30 AM
MARKET_CLOSE = dtime(16, 0)   # 4:00 PM

# Date range this will run (12-01-2025 to 12-05-2025) 
START_DATE = date(2025, 12, 1)    
END_DATE   = date(2025, 12, 5)    

# Initialize Alpaca data fetcher
alpaca_fetcher = AlpacaDataFetcher(ticker="AAPL", timeframe_minutes=1)
last_fetch_time = None

# Initialize Alpaca API for order execution
alpaca_api = tradeapi.REST(
    key_id=os.getenv('KEY_ID'),
    secret_key=os.getenv('SECRET_KEY'),
    base_url='https://paper-api.alpaca.markets',
    api_version='v2'
)

# Trading state
current_position = 0  # 0 = flat, 1 = long, -1 = short
last_signal = 0
trade_log = []    

# Signal history for tracking
signal_history = []  # List of (timestamp, signal) tuples


def get_account_info():
    """Fetch and display current account balance and positions."""
    try:
        account = alpaca_api.get_account()
        print(f"  Account Balance: ${float(account.cash):.2f}")
        print(f"  Portfolio Value: ${float(account.portfolio_value):.2f}")
        print(f"  Buying Power: ${float(account.buying_power):.2f}")
        return account
    except Exception as e:
        print(f"[ERROR] Failed to fetch account: {e}")
        return None


def submit_order(symbol, qty, side):
    """Wrapper to submit orders (respects DRY_RUN). Returns an object with `.id`."""
    if DRY_RUN:
        print(f"  [DRY_RUN] Would submit {side.upper()} {qty} {symbol}")
        return SimpleNamespace(id=f"DRY-{int(time.time())}")
    else:
        return alpaca_api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='day'
        )


def get_position_qty(symbol):
    """Return integer quantity of current position for symbol, or 0 if none."""
    try:
        pos = alpaca_api.get_position(symbol)
        return int(float(pos.qty))
    except Exception:
        return 0


def execute_trade(signal, latest_price, timestamp):
    """Execute buy/sell orders based on momentum signal."""
    global current_position, last_signal, trade_log
    
    ticker = 'AAPL'
    
    # Only trade if signal changes (avoid multiple orders on same signal)
    if signal == last_signal:
        print(f"  [NO CHANGE] Signal {signal:+d} same as last {last_signal:+d}, NO TRADE")
        return
    
    # Signal CHANGED!
    print(f"  *** SIGNAL CHANGED: {last_signal:+d} → {signal:+d} ***")
    last_signal = signal
    
    try:
        if signal == 1 and current_position != 1:
            # BUY signal
            print(f"  [SIGNAL] BUY at ${latest_price:.2f}")
            order = submit_order(ticker, 20, 'buy')
            current_position = 1
            trade_log.append({
                'timestamp': timestamp,
                'action': 'BUY',
                'price': latest_price,
                'qty': 20,
                'order_id': order.id
            })
            print(f"  ✓ Buy order submitted: {order.id}")

        elif signal == -1 and current_position != -1:
            # SELL signal
            print(f"  [SIGNAL] SELL at ${latest_price:.2f}")
            order = submit_order(ticker, 20, 'sell')
            current_position = -1
            trade_log.append({
                'timestamp': timestamp,
                'action': 'SELL',
                'price': latest_price,
                'qty': 20,
                'order_id': order.id
            })
            print(f"  ✓ Sell order submitted: {order.id}")

        elif signal == 0:
            # Neutral signal: close existing position if any
            # Close position using actual position size if available
            qty = get_position_qty(ticker)
            if qty > 0 and current_position == 1:
                print(f"  [SIGNAL] NEUTRAL - closing LONG position of {qty} at ${latest_price:.2f}")
                order = submit_order(ticker, qty, 'sell')
                trade_log.append({
                    'timestamp': timestamp,
                    'action': 'CLOSE_LONG',
                    'price': latest_price,
                    'qty': qty,
                    'order_id': order.id
                })
                print(f"  ✓ Close long submitted: {order.id}")
                current_position = 0
            elif qty > 0 and current_position == -1:
                print(f"  [SIGNAL] NEUTRAL - closing SHORT position of {qty} at ${latest_price:.2f}")
                order = submit_order(ticker, qty, 'buy')
                trade_log.append({
                    'timestamp': timestamp,
                    'action': 'CLOSE_SHORT',
                    'price': latest_price,
                    'qty': qty,
                    'order_id': order.id
                })
                print(f"  ✓ Close short submitted: {order.id}")
                current_position = 0

    except Exception as e:
        print(f"  [ERROR] Failed to execute trade: {e}")


def do_work():
    """Execute trading logic: fetch live data, generate signals, and trade."""
    global last_fetch_time
    
    now = datetime.now(MARKET_TZ)
    
    # Fetch fresh AAPL data from Alpaca every minute (or on first run)
    should_fetch = (last_fetch_time is None or 
                   (now - last_fetch_time).total_seconds() > 60)
    
    if should_fetch:
        print(f"\n[{now}] === MARKET DATA UPDATE ===")
        csv_path = alpaca_fetcher.fetch_and_save(lookback_days=7)
        if csv_path:
            last_fetch_time = now
        else:
            print("[ERROR] Failed to fetch data from Alpaca")
            return
    else:
        csv_path = str(alpaca_fetcher.csv_path)
    
    # Load the CSV data
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from AAPL_live.csv")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return
    
    # Generate momentum signals
    momentum = Momentum(df)
    signals = momentum.run()
    
    # Get latest signal (most recent timestamp)
    if signals and len(signals) > 0:
        latest_idx = max(signals.keys())
        latest_signal = signals[latest_idx]
        
        # Get latest price
        latest_row = df.iloc[-1]
        latest_price = latest_row['Close']
        latest_time = latest_row['Datetime']
        
        print(f"Latest Signal: {latest_signal:+d} | Price: ${latest_price:.2f} | Time: {latest_time}")
        
        # Track signal history: append only when timestamp advances.
        # If timestamp is identical but signal changed, update last entry.
        if not signal_history or signal_history[-1][0] != latest_time:
            signal_history.append((latest_time, latest_signal))
        else:
            # same timestamp — update signal if it changed
            if signal_history[-1][1] != latest_signal:
                signal_history[-1] = (latest_time, latest_signal)

        # Show last 5 signals for reference
        print(f"Signal History (last 5):")
        for ts, sig in signal_history[-5:]:
            marker = "← CURRENT" if sig == latest_signal else ""
            print(f"  {ts}: {sig:+d} {marker}")

        # Execute trade based on signal (execute_trade will skip if no change)
        execute_trade(latest_signal, latest_price, latest_time)
    
    # Show account status
    print("Account Status:")
    get_account_info()
    
    # Save trade log
    if trade_log:
        trade_df = pd.DataFrame(trade_log)
        trade_df.to_csv('trade_log.csv', index=False)
        print(f"Trades logged: {len(trade_log)}")


# ---- MAIN LOOP ----
base = str(Path(__file__).resolve().parent)+'/'
directory = f'{base}data/'

while True:
    now = datetime.now(MARKET_TZ)
    today = now.date()
    current_time = now.time()
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    # Stop completely after the end date
    if today > END_DATE:
        print("End date passed. Exiting script.")
        break

    # Check if we are within the desired date range
    in_date_range = START_DATE <= today <= END_DATE

    # Check if it's a weekday (Mon–Fri)
    is_weekday = weekday < 5

    # Check if we're within market hours
    in_market_hours = MARKET_OPEN <= current_time <= MARKET_CLOSE

    if in_date_range and is_weekday and in_market_hours:
        do_work()
    else:
        # do nothing out of market hours 
        pass

    time.sleep(60)   # sleep for 10 seconds before loop restarts
