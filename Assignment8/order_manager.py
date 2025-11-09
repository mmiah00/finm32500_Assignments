# Receives and logs executed trades
import socket
import threading
import json

MESSAGE_DELIMITER = b"*_*"
HOST = "127.0.0.1"
PORT = 9100


class OrderManager:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.order_id = 0
        self.running = True

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"[OrderManager] Listening on {self.host}:{self.port}...")

        try:
            while self.running:
                conn, addr = server_socket.accept()
                print(f"[OrderManager] Connection from {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn,))
                client_thread.start()
        except KeyboardInterrupt:
            print("[OrderManager] Shutting down server...")
        finally:
            server_socket.close()

    def handle_client(self, conn):
        # handle incoming messages from Strategy client 
        with conn:
            buffer = b""
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data

                # Process each complete message (split by delimiter)
                while MESSAGE_DELIMITER in buffer:
                    msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                    if msg:
                        self.process_order(msg)

    def process_order(self, msg_bytes):
        # log order 
        try:
            order = json.loads(msg_bytes.decode("utf-8"))
            self.order_id += 1
            symbol = order.get("Symbol", "UNKNOWN")
            side = order.get("Side", "UNKNOWN").upper()
            price = order.get("Price", 0.0)
            qty = order.get("Qty", 10)  # default to 10 shares if not included
            print(f"Received Order {self.order_id}: {side} {qty} {symbol} @ {price:.2f}")
        except json.JSONDecodeError as e:
            print(f"[OrderManager] Failed to decode order: {e}")


def run_ordermanager():
    om = OrderManager()
    om.start_server()


if __name__ == "__main__":
    run_ordermanager()

