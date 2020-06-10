# Import package
import yfinance as yf

tickers = ["AAPL", "TD", "M", "CPG", "CM", "HTZ", "LK", "OAS", "XSPA", "VAL", "VISL", "GNUS", "NE", "FRSX","GCI","SRNE","LTM","DGLY","TUES","BIOL","CBL","CIDM","MARK","CHAP","NSPR"]
for ticker in tickers:
    # Get the data
    data = yf.download(tickers=ticker, period="7d", interval="1m")

    # Print the data
    with open('data/'+ticker+'.csv', 'w') as writer:
        for key, value in data.get('Close').items():
            writer.write(str(key) + ', ' + str(value) + "\n")