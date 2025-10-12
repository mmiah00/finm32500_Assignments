from dataclasses import dataclass
from abc import ABC, abstractmethod
from data_loader import MarketDataPoint


@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass