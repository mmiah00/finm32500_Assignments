from feature_engineering import FeatureEngineering
from train_model import ModelRunner


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
    runner = ModelRunner()

    bst = runner.run_xgb()
    runner.run_logistic()       
    runner.run_cross_val(bst)    

    