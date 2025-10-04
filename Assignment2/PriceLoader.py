import pandas as pd 
import yfinance as yf 
import requests
    
class PriceLoader: 

    def __init__ (self, filepath="data/", start="2005-01-01", end="2025-01-01", tickers =[]): 
        self.filepath = filepath 
        self.start_date = start 
        self.end_date = end 
        self.tickers = tickers 
    
    def load_tickers(self, tickers_url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"): 
        # given a url tickers_url with a list of all the tickers that you are interested in pulling, add those tickers from the url to self.tickers
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        try:
            response = requests.get(tickers_url, headers=headers)
            response.raise_for_status()  # raise an error if request fails

            # read HTML tables from the page content
            tables = pd.read_html(response.text)

            # the first table contains the tickers
            tickers_ = tables[0]["Symbol"].to_list()

            # adjust ticker format for yfinance (replace '.' with '-')
            tickers_ = [t.replace(".", "-") for t in tickers_]

            self.tickers = tickers_
            print(f"Loaded {len(self.tickers)} tickers successfully.")
            return self.tickers

        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
        except Exception as e:
            print(f"Error loading tickers: {e}")

    
    def download_ticker_prices(self, batch_size=25): 
        if self.tickers: # make sure tickers is not empty 

            i = 0 
            file_num = 1
            while i < len(self.tickers): 
                print(f"Downloading batch {file_num}")
                tickers_batch = self.tickers[i:i+batch_size]
                data = yf.download(tickers=tickers_batch, start = self.start_date, end=self.end_date, group_by="ticker", auto_adjust=True)
                

                # download each ticker in its own file 
                for ticker in tickers_batch: 
                    try: 

                        df = data[ticker]
                        # print(df.head(5))
                        df = df[['Close']]
                        df = df.dropna() # drop null values 
                        
                        # save to its own file 
                        filename = f"{self.filepath}{ticker}_{self.start_date}_to_{self.end_date}.parquet" 
                        df.to_parquet(filename)
                    except Exception as e:
                        print(f"Error saving {ticker} data: {e}")
                
                i += batch_size 
                file_num += 1

    def get_ticker_data (self, ticker, path): 
        # read in data of given ticker from data in local storage @ location path
        
        # if not path.exists():
        #     raise FileNotFoundError(f"No data file found for {ticker}")
        # return pd.read_parquet(filepath)

        try: 
            return pd.read_parquet(path)
        except FileNotFoundError as e: 
            print (f"File at location \'{path}\' not found for {ticker}")
    
    def get_select_ticker_data (self, tickers): 
        # can be used to get dataframe data for all tickers or of select group of tickers as specified by the tickers argument 
        dfs = {}
        for t in tickers:
            try:
                path = f"{self.filepath}{t}_{self.start_date}_to_{self.end_date}.parquet" 
                dfs[t] = self.get_ticker_data(t, path)["Close"]
            except FileNotFoundError:
                print(f"Missing {t}")
        return pd.DataFrame(dfs) # returns a dictionary of key = ticker name (str) and value = ticker prices (Pandas Series)
 
    
if __name__ == "__main__":
    loader = PriceLoader()
    ticks = loader.load_tickers() 

    loader.download_ticker_prices() 
    data = loader.get_select_ticker_data(loader.tickers)
    
    # for ticker in data: 
    #     ticker_data = data[ticker]
    #     print(ticker_data.head())
    #     print("===========")

