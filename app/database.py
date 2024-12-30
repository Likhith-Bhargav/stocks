import psycopg2
from app.config import DATABASE

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DATABASE)

    def insert_stock_data(self, stock_name, starting_date, starting_price, data):
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            cursor.execute("""
                INSERT INTO stock_data (stock_name, starting_date, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                stock_name,
                starting_date,
                row['Date'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume']
            ))
        self.conn.commit()
        cursor.close()

    def store_plot_in_database(self, stock_name, starting_date, plot_base64):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE stock_data
            SET plot_base64 = %s
            WHERE stock_name = %s AND starting_date = %s
        """, (plot_base64, stock_name, starting_date))
        self.conn.commit()
        cursor.close()

    def close(self):
        self.conn.close()
