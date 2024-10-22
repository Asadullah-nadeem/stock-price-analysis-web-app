from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

app = Flask(__name__)

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def plot_stock_data(stock_data):
    fig = px.line(stock_data, x=stock_data.index, y='Close', labels={'y': 'Stock Price'})
    fig.update_layout(
        title='Stock Price Analysis',
        xaxis_title='Date',
        yaxis_title='Stock Price',
        showlegend=True,
        xaxis_rangeslider_visible=True, 
    )

    plot_html = fig.to_html(full_html=False)

    return plot_html

def calculate_returns(stock_data):
    stock_data['Daily Return'] = stock_data['Close'].pct_change()
    return stock_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_ticker = request.form['stock_ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        stock_data = get_stock_data(stock_ticker, start_date, end_date)

        plot_html = plot_stock_data(stock_data)

        stock_data = calculate_returns(stock_data)
        
        return render_template('index.html', plot_html=plot_html, stock_data=stock_data[['Close', 'Daily Return']].head().to_html())

    return render_template('index.html', plot_html=None, stock_data=None)

if __name__ == '__main__':
    app.run(debug=True)