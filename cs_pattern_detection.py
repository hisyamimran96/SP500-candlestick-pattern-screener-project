import talib
import yfinance as yf

data = yf.download("SPY", start = "2023-01-01", end = "2023-02-01")

morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

print(morning_star)
