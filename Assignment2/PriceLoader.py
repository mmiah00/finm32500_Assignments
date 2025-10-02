import pandas as pd 
import yfinance as yf 

class PriceLoader: 

    def __init__ (self, filepath="data/", start="2005-01-01", end="2025-01-01", tickers =[]): 
        self.filepath = filepath 
        self.start_date = start 
        self.end_date = end 
        self.tickers = tickers 
    
    def load_tickers(self, list_of_tickers=""): 
        # given a url list_of_tickers with a list of all the tickers that you are interested in pulling, add those tickers from the url to self.tickers
        tables = pd.read_html(list_of_tickers)
        tickers_ = tables[0]["Symbol"].to_list()
        tickers_ = [t.replace(".", "-") for t in tickers_]  # adjust ticker names for consistenc
        self.tickers = tickers_ 
    
    def download_ticker_prices(self, batch_size=25): 
        if tickers: # make sure tickers is not empty 

            i = 0 
            file_num = 1
            while i < len(self.tickers): 
                tickers_batch = self.tickers[i:i+batch_size]
                data = yf.download(tickers=self.tickers, start = self.start_date, end=self.end_date, group_by="ticker", auto_adjust=True)
                

                # download each ticker in its own file 
                for ticker in tickers_batch: 
                    try: 

                        df = data[ticker]
                        df = df['Adj Close']
                        df = df.dropna() # drop null values 
                        
                        # save to its own file 
                        filename = f"{self.filepath}{ticker}_{self.start_date}_to_{self.end_date}.parquet" 
                        df.to_parquet(filename)
                    except Exception as e:
                        print(f"Error saving {ticker} data: {e}")
                
                i += batch_size 

    def get_ticker_data (self, ticker, path): 
        # read in data of given ticker from data in local storage @ location path
        if not path.exists():
            raise FileNotFoundError(f"No data file found for {ticker}")
        return pd.read_parquet(filepath)
    
    def get_select_ticker_data (self, tickers): 
        dfs = {}
        for t in tickers:
            try:
                dfs[t] = self.load(t)["AdjClose"]
            except FileNotFoundError:
                print(f"Missing {t}")
        return pd.DataFrame(dfs) 
