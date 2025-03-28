class DataLoader:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def load_data(self):
        import yfinance as yf
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return self.data

    def preprocess_data(self):
        if self.data is not None:
            # Example preprocessing: fill missing values and normalize
            self.data.fillna(method='ffill', inplace=True)
            self.data['Return'] = self.data['Close'].pct_change()
            self.data.dropna(inplace=True)
            return self.data
        else:
            raise ValueError("Data not loaded. Call load_data() first.")