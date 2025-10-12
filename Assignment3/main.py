from data_loader import load_data
from strategies import NaiveMovingAverageStrategy, WindowedMovingAverageStrategy

sample_data = load_data (200)

naive_strat = NaiveMovingAverageStrategy(window_size=20)
windowed_strat = WindowedMovingAverageStrategy(window_size=20)

native_strat.generate_signals (sample_data) 
windowed_strat.generate_signals (sample_data)
