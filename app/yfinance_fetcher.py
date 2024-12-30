import yfinance as yf
import pandas as pd

class YFinanceFetcher:
    @staticmethod
    def fetch_stock_data(stock_name):
        stock = yf.Ticker(stock_name)
        data = stock.history(period="max")  # Get maximum historical data
        data.reset_index(inplace=True)  # Reset index for easy access
        return data
