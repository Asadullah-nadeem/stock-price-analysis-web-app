import requests
import logging
from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

app = Flask(__name__)

if not os.path.exists('log'):
    os.makedirs('log')

log_file_name = os.path.join('log', f"{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_file_name,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        stock_info = yf.Ticker(ticker).info
        if stock_data.empty:
            raise ValueError(f"No data found for {ticker}. Please check the stock ticker and date range.")
        
        logging.info(f'Successfully retrieved stock data for {ticker} from {start_date} to {end_date}')
        
        return stock_data, {
            "exchangeTimezoneName": stock_info.get("exchangeTimezoneName", "N/A"),
            "regularMarketPrice": stock_info.get("regularMarketPrice", "N/A"),
            "fiftyTwoWeekHigh": stock_info.get("fiftyTwoWeekHigh", "N/A"),
            "fiftyTwoWeekLow": stock_info.get("fiftyTwoWeekLow", "N/A"),
            "regularMarketDayHigh": stock_info.get("regularMarketDayHigh", "N/A"),
            "regularMarketDayLow": stock_info.get("regularMarketDayLow", "N/A"),
            "longName": stock_info.get("longName", "N/A"),
            "shortName": stock_info.get("shortName", "N/A"),
            "chartPreviousClose": stock_info.get("chartPreviousClose", "N/A"),
            "previousClose": stock_info.get("previousClose", "N/A"),
        }
    except Exception as e:
        logging.error(f'Error retrieving stock data for {ticker}: {str(e)}')
        raise


def plot_stock_data(stock_data):
    try:
        if 'Close' not in stock_data:
            raise ValueError("The 'Close' column is missing in the stock data.")

        close_prices = stock_data['Close'].squeeze()

        fig = px.line(stock_data, x=stock_data.index, y=close_prices, labels={'y': 'Stock Price'})
        fig.update_layout(
            title='Stock Price Analysis',
            xaxis_title='Date',
            yaxis_title='Stock Price',
            showlegend=True,
            xaxis_rangeslider_visible=True, 
        )
        logging.info('Successfully generated stock plot')
        plot_html = fig.to_html(full_html=False)
        return plot_html
    except Exception as e:
        logging.error(f'Error generating stock plot: {str(e)}')
        raise

def calculate_returns(stock_data):
    try:
        stock_data['Daily Return'] = stock_data['Close'].pct_change()
        logging.info('Successfully calculated daily returns')
        return stock_data
    except Exception as e:
        logging.error(f'Error calculating daily returns: {str(e)}')
        raise

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_ticker = request.form['stock_ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        logging.info(f'Form submitted with ticker: {stock_ticker}, start date: {start_date}, end date: {end_date}')
        
        if start_date > end_date:
            error_message = "Start date cannot be after end date."
            logging.error(f'Invalid date range: {error_message}')
            return render_template('stock_calculator.html', plot_html=None, stock_data=None, error=error_message)
        
        try:
            stock_data, additional_info = get_stock_data(stock_ticker, start_date, end_date)
            plot_html = plot_stock_data(stock_data)
            stock_data = calculate_returns(stock_data)

            logging.info('Rendered template with stock data and plot')
            return render_template('stock_calculator.html', plot_html=plot_html, stock_data=stock_data[['Close', 'Daily Return']].head().to_html(), additional_info=additional_info)
        
        except Exception as e:
            logging.error(f'An error occurred in the index route: {str(e)}')
            return render_template('stock_calculator.html', plot_html=None, stock_data=None, error=str(e))
    
    return render_template('stock_calculator.html', plot_html=None, stock_data=None)

# @app.route('/today-stock')
# def today_stock():
#         return render_template('today_stock.html',)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    logging.info('Starting the Flask app')
    app.run(debug=True)
