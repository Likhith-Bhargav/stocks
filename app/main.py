import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.yfinance_fetcher import YFinanceFetcher
from app.database import Database
from app.plot_generator import PlotGenerator

def main():
    # User input for stock symbol
    stock_name = input("Enter stock symbol: ")

    # Fetch stock data from yfinance
    print(f"Fetching data for {stock_name}...")
    data = YFinanceFetcher.fetch_stock_data(stock_name)

    if data.empty:
        print(f"No data found for the stock symbol: {stock_name}.")
        return

    # Starting date and starting price (first row of fetched data)
    starting_date = data['Date'].iloc[0]
    starting_price = data['Open'].iloc[0]

    # Save data to the database
    db = Database()
    try:
        print("Storing data in the database...")
        db.insert_stock_data(stock_name, starting_date, starting_price, data)

        # Generate and store the plot
        print("Generating and storing plot...")
        plot_base64 = PlotGenerator.generate_plot_base64(data, stock_name)
        db.store_plot_in_database(stock_name, starting_date, plot_base64)

        print("Data and plot stored successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
