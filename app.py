from flask import Flask, render_template, request
from patterns import candlestick_patterns
import yfinance as yf
import os
import csv
import pandas as pd
import talib
from datetime import date
from dateutil.relativedelta import relativedelta


app = Flask(__name__)

@app.route("/")
def mainpage():
    pattern = request.args.get('pattern', None) #get request information, in this case we want the name of the pattern.
    stocks = {}
    
    with open('datasets/sp500.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        filename = os.listdir('datasets/daily')
        for file in filename:
            df = pd.read_csv('datasets/daily/{}'.format(file))
            patfunc = getattr(talib, pattern)
            symbol = file.split('.')[0]

            try:
                result = patfunc(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]
                if last > 0:
                    stocks[symbol][pattern] = 'Bullish {}'.format(candlestick_patterns[pattern])
                elif last < 0:
                    stocks[symbol][pattern] = 'Bearish {}'.format(candlestick_patterns[pattern])
                else:
                    stocks[symbol][pattern] = None    
            except:
                pass

    return render_template('index.html', patterns = candlestick_patterns, stocks = stocks, pattern_ = pattern) #send variable to html template

@app.route("/updateprice")
def snapshot():
    with open('datasets/sp500.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            end_date = date.today()
            start_date = end_date - relativedelta(months = 3)
            df = yf.download(symbol, start = start_date, end = end_date)
            df.to_csv('datasets/daily/{}.csv'.format(symbol))


    return "Successfully update stock prices."

if __name__ == '__main__':
    app.run(debug=True)