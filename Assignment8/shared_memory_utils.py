# Defines shared memory wrapper
import numpy as np
from multiprocessing import shared_memory, Lock


class SharedPriceBook:
    def __init__(self, symbols, name=None, create=True, lock=None):
        self.symbols = symbols
        self.lock = lock or Lock()
        self.dtype = np.float64
        self.shape = (len(symbols),)
        self.size = np.prod(self.shape) * np.dtype(self.dtype).itemsize

        if create:
            # Create new shared memory block
            self.shm = shared_memory.SharedMemory(create=True, size=self.size, name=name)
            self.array = np.ndarray(self.shape, dtype=self.dtype, buffer=self.shm.buf)
            self.array[:] = np.nan  # initialize with NaN
        else:
            # Attach to an existing shared memory block
            self.shm = shared_memory.SharedMemory(name=name)
            self.array = np.ndarray(self.shape, dtype=self.dtype, buffer=self.shm.buf)

        # Map symbol → index  
        self.index_map = {symbol: i for i, symbol in enumerate(symbols)}

    def update(self, symbol, price):
        # update shared memory with updated prices 
        if symbol not in self.index_map:
            raise KeyError(f"Symbol {symbol} not found in shared price book.")

        idx = self.index_map[symbol]
        with self.lock:
            self.array[idx] = price

    def read(self, symbol):
        if symbol not in self.index_map:
            raise KeyError(f"Symbol {symbol} not found.")
        idx = self.index_map[symbol]
        return float(self.array[idx])

    def read_all(self):
        # returns a dictionary of all prices as {symbol: price} for all symbols
        with self.lock:
            return {sym: float(self.array[i]) for i, sym in enumerate(self.symbols)}

    def close(self):
        # detach from shared memory 
        self.shm.close()

    def unlink(self):
        # destroys shared memory block 
        self.shm.unlink()
