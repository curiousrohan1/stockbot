from pandas_datareader import data as pdr
from datetime import datetime
import time
import yfinance as yf
import sqlite3

yf.pdr_override()
# noinspection SpellCheckingInspection
tickers = ['HTZ', 'LK', 'OAS', 'XSPA', 'VAL', 'VISL', 'GNUS', 'NE', 'FRSX', 'GCI',
           'SRNE', 'LTM', 'DGLY', 'TUES', 'BIOL', 'CBL', 'CIDM', 'MARK', 'CHAP', 'NSPR']
# noinspection SpellCheckingInspection
conn = sqlite3.connect('../../Documents/stockbot')


def get_data(ticker_list):
    now = datetime.now()
    cur_date = now.strftime('%Y-%m-%d')
    cur_time = now.strftime('%H:%M')

    if '06:30' <= cur_time <= '13:00':
        data = pdr.get_quote_yahoo(ticker_list)
        c = conn.cursor()
        for symbol, price in data.get('price').items():
            c.execute("INSERT INTO QUOTES VALUES (?, ?, ?, ?)",
                      (cur_date, cur_time, symbol, price))
        conn.commit()


try:
    while True:
        get_data(tickers)
        time.sleep(60)
except KeyboardInterrupt:
    conn.close()
