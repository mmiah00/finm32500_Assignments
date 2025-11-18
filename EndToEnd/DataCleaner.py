import pandas as pd

class Cleaner:
    def __init__(self, name):
        self.df = self.create_df(name)
        self.name = name
        self.remove()
        self.datetime_sort()
        self.save_cleaned()
        self.print()

    def print(self):
        print(self.df)

    def create_df(self,name):
        self.df = pd.read_parquet(path=f'EndToEnd/data/{name}.parquet')
        return self.df

    def remove(self):
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates()
        return self.df

    def datetime_sort(self):
        is_datetime = isinstance(self.df.index, pd.DatetimeIndex)
        if is_datetime is False:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df = self.df.set_index('Date')
        self.df = self.df.sort_index()
        return self.df

    def derived_features(self):
        pass

    def save_cleaned(self):
        self.df.to_parquet(path=f'EndToEnd/cleaned/{self.name}.parquet')
        return self.df


if __name__ == "__main__":
    name = 'AAPL_2005-01-01_to_2025-01-01'
    cleaner = Cleaner(name)