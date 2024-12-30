import base64
import io
import matplotlib.pyplot as plt

class PlotGenerator:
    @staticmethod
    def generate_plot_base64(data, stock_name):
        # Create plot for Closing Price vs Date
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['Close'], label='Closing Price', color='blue')
        plt.title(f'Closing Price vs Date for {stock_name}')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.legend()
        plt.grid(True)

        # Convert plot to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()
        return plot_base64
