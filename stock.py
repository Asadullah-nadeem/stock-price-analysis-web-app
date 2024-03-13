import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def plot_stock_data(stock_data):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label='Close Price', marker='o') 

    for i, value in enumerate(stock_data['Close']):
        plt.annotate(f'{value:.2f}', (stock_data.index[i], value), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title('Stock Price Analysis')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

def calculate_returns(stock_data):
    stock_data['Daily Return'] = stock_data['Close'].pct_change()
    return stock_data

def main():
    stock_ticker = 'SUZLON.NS' 
    start_date = '2024-01-30'
    end_date = '2024-02-10'

    stock_data = get_stock_data(stock_ticker, start_date, end_date)

    plot_stock_data(stock_data)

    stock_data = calculate_returns(stock_data)
    print(stock_data[['Close', 'Daily Return']].head())

if __name__ == "__main__":
    main()
