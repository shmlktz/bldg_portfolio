# 4 lines of code; candlestick charts
#not including lines 1 and 2 which are comments
#or line three = ) #or line four which I'll leave blank for styling

import mplfinance as mpf
from pandas_datareader import data
df = data.DataReader("aapl", "yahoo", start = "01-01-1980")
mpf.plot(df, type= "candle", ylabel = "Price USD", title= "AAPL Share Price", volume = True, mav=(20,50), style="yahoo")