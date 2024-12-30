import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class YFinanceFetcher:
    def fetch_data(self, stock_name):
        data = yf.download(stock_name, start="2022-01-01", end=str(datetime.date.today()))

        stock_data = {
            'start_date': data.index[0].strftime('%Y-%m-%d'),
            'start_price': data['Open'].iloc[0],
            'high': data['High'].max(),
            'low': data['Low'].min(),
            'open': data['Open'].iloc[-1],
            'close': data['Close'].iloc[-1],
            'volume': data['Volume'].iloc[-1],
            'plot': self.generate_plot(data, stock_name)
        }
        return stock_data

    def generate_plot(self, data, stock_name):
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'], label="Closing Price", color='blue')
        plt.title(f"Closing Price for {stock_name}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        return plot_base64
