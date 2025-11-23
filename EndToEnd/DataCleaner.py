import pandas as pd
import numpy as np
import os

class Cleaner:
    def __init__(self, name):
        self.name = name
        self.df = self.create_df(name)
        self.datetime_sort()
        self.derived_features()
        self.remove()
        self.save_cleaned()
        # self.print()

    def create_df(self,name):
        self.df = pd.read_csv(f'EndToEnd/data/{name}')
        # self.datetime_sort() 
        return self.df

    def remove(self):
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()
        return self.df

    def datetime_sort(self):
        is_datetime = isinstance(self.df.index, pd.DatetimeIndex)
        if is_datetime is False:
            self.df['Datetime'] = pd.to_datetime(self.df['Datetime'])
            self.df = self.df.set_index('Datetime')
        self.df = self.df.sort_index()
        return self.df

    def derived_features(self):
        self.df['Minute Returns'] = self.df['Close'].pct_change()
        self.df['Rolling 5 Minute Returns'] = (1+self.df['Minute Returns']).rolling(window=5).apply(np.prod, raw=True) - 1
        self.df['20 Minute Moving Average'] = (self.df['Minute Returns']).rolling(window=20).mean()
        self.df['50 Minute Moving Average'] = (self.df['Minute Returns']).rolling(window=50).mean()
        return self.df

    def save_cleaned(self):
        self.df.to_csv(f'EndToEnd/cleaned/{self.name}_cleaned.csv')
        return self.df
    
    def print(self):
        print(self.df)
        return self.df


# if __name__ == "__main__":
#     directory = '/Users/ericbeechen/Documents/GitHub/finm32500_Assignments/EndToEnd/data/'
#     names = []
#     for entry in os.scandir(directory):
#         names.append(entry.name)
#     for name in names:    
#         cleaner = Cleaner(name)