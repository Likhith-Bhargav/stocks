import os
import psycopg2
from dotenv import load_dotenv
from app.config import DATABASE
import base64

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.conn.cursor()

    def get_stock_data(self, stock_name):
        query = "SELECT * FROM stock_data WHERE stock_name = %s"
        self.cursor.execute(query, (stock_name,))
        result = self.cursor.fetchone()
        if result:
            return {
                'stock_name': result[1],
                'start_date': result[2],
                'start_price': result[3],
                'high': result[6],
                'low': result[7],
                'open': result[5],
                'close': result[8],
                'volume': result[9],
                'plot': result[10]
            }
        return None

    def save_stock_data(self, stock_name, data):
        query = """
        INSERT INTO stock_data (stock_name, start_date, start_price, high, low, open, close, volume, plot)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            stock_name, data['start_date'], data['start_price'], data['high'], data['low'],
            data['open'], data['close'], data['volume'], data['plot']
        ))
        self.conn.commit()
