from feature_engineering import FeatureEngineering
from train_model import ModelRunner
from signal_generator import Signals


class Backtest:
    def __init__(self):
        pass

    def simulate(self):
        pass

    def plot(self):
        pass


if __name__ == "__main__":
    fe = FeatureEngineering()
    market_data_df = fe.run()

    runner = ModelRunner(df=market_data_df)

    bst = runner.run_xgb()
    log = runner.run_logistic()       
    runner.run_cross_val(bst)    

    bst_signals = Signals(bst, low_threshold=0.4, high_threshold=0.6).generate(market_data_df['close'])
    log_signals = Signals(log, low_threshold=0.45, high_threshold=0.55).generate(market_data_df['close'])
    print(bst_signals['signals'].count("BUY"), log_signals['signals'].count("BUY"))