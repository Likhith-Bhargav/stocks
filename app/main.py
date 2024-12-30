import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, request, jsonify
from yfinance_fetcher import YFinanceFetcher
from database import Database
from plot_generator import PlotGenerator
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)
db = Database()
yf_fetcher = YFinanceFetcher()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    stock_name = request.form.get('stock_name')

    # Check if stock data exists in the database
    stock_data = db.get_stock_data(stock_name)

    if stock_data:
        # Stock data exists, decode the plot from base64
        plot_base64 = stock_data['plot']
    else:
        # Stock data does not exist, fetch from yfinance and save to the database
        data = yf_fetcher.fetch_data(stock_name)
        db.save_stock_data(stock_name, data)
        plot_base64 = data['plot']

    # Render the stock data and plot
    return render_template('stock_data.html', stock_data=stock_data or data, plot_base64=plot_base64)

if __name__ == '__main__':
    app.run(debug=True)
