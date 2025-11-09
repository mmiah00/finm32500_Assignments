# Launches all processes
# main.py
from multiprocessing import Process
import time

from gateway import run_gateway
from orderbook import run_orderbook
from strategy import run_strategy
from order_manager import run_ordermanager


def main():
    # Gateway → OrderBook → Strategy → OrderManager
    processes = []

    try:
        print("Starting trading system...")

        # start Gateway  
        gateway_proc = Process(target=run_gateway, name="Gateway")
        gateway_proc.start()
        processes.append(gateway_proc)
        print("Gateway started.")
        time.sleep(1.5)  # Give the server time to bind to port

        # start OrderBook 
        orderbook_proc = Process(target=run_orderbook, name="OrderBook")
        orderbook_proc.start()
        processes.append(orderbook_proc)
        print("OrderBook started.")
        time.sleep(1.0)

        # start Strategy 
        strategy_proc = Process(target=run_strategy, name="Strategy")
        strategy_proc.start()
        processes.append(strategy_proc)
        print("Strategy started.")
        time.sleep(1.0)

        # start OrderManager 
        ordermanager_proc = Process(target=run_ordermanager, name="OrderManager")
        ordermanager_proc.start()
        processes.append(ordermanager_proc)
        print("OrderManager started.")

        print("All processes running. To manually stop, press Ctrl+C to stop.")

        # Wait for all to finish (blocks until manual stop)
        for p in processes:
            p.join()

    except KeyboardInterrupt: 
        # handling if Ctrl+C is pressed 
        print("\nKeyboardInterrupt detected — shutting down gracefully...")
        for p in processes:
            if p.is_alive():
                print(f"Terminating {p.name}...")
                p.terminate()
        print("All processes terminated.")


if __name__ == "__main__":
    main()
