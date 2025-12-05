from feature_engineering import FeatureEngineering
from train_model import ModelRunner
from signal_generator import Signals
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt


class Backtest:
    def __init__(self, df):
        self.size = 1
        self.costs = 0
        self.df = df
        self.positions = {t: 0 for t in self.df['ticker'].unique()}
        self.value = {t: 0 for t in self.df['ticker'].unique()}
        self.average = {t: 0 for t in self.df['ticker'].unique()}
        self.cash = 100000
        self.pnl = 0
        self.pnls = {}

    def simulate(self, strategy):
        for index, row in self.df.iterrows():
            print(row)
            price = row['close']
            ticker = row['ticker']
            signal = row[f'{strategy} signals']
            if signal == 'BUY':
                self.positions[ticker] += 1
                self.value[ticker] += price
                if self.positions[ticker] != 0:
                    self.pnl += self.average[ticker] - self.value[ticker]/self.positions[ticker]
                    self.average[ticker] = self.value[ticker]/self.positions[ticker]
                self.cash -= price
            elif signal == 'SELL':
                self.positions[ticker] -= 1
                self.value[ticker] -= price
                if self.positions[ticker] != 0:
                    self.pnl += self.average[ticker] + self.value[ticker]/self.positions[ticker]
                    self.average[ticker] = self.value[ticker]/self.positions[ticker]
                self.cash += price
            self.pnls[index] = self.pnls.get(index, 0) + self.pnl
        return self

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
    market_data_df['bst signals'] = bst_signals['signals']
    bt = Backtest(market_data_df)
    bt.simulate('bst')
    # print(bt.positions, bt.average, bt.pnl)
    plt.plot(bt.pnls.keys(), bt.pnls.values())
    plt.show()
    # print(bst_signals['signals'].count("BUY"), log_signals['signals'].count("BUY"))