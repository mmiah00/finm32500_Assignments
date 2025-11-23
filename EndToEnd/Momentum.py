class Momentum:
    def __init__(self, df):
        self.df = df
        # self.df.set_index('Datetime', inplace=True)

    def run(self): 
        buy_signals = {}
        for index, row in self.df.iterrows():
            if row['20 Minute Moving Average'] > row['50 Minute Moving Average']:
                buy_signals[index] = 1 #row['Close']
            elif row['20 Minute Moving Average'] < row['50 Minute Moving Average']:
                buy_signals[index] = -1 # short 
            else: 
                buy_signals[index] = 0  # don't hold 
        return buy_signals

