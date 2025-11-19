class Momentum:
    def __init__(self, df):
        self.df = df

    def run(self): 
        buy_signals = {}
        for index, row in self.df.iterrows():
            if row['20 Minute Moving Average'] > row['50 Minute Moving Average']:
                buy_signals[index] = row['Close']
        return buy_signals

