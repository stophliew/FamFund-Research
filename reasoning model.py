import yfinance as yf
import pandas as pd
import time

sp500_list = pd.read_html("https://en.wikipedia.org/wikiList_of_S%26P_500_companies")
sp500 = sp500_list[0]
sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=False)
symbol_list = sp500["Symbol"].unique().tolist()


# generate the income statement based on base model's evals
income_statement = {}

for symbol in symbol_list[:20]:
    stock = yf.Ticker(symbol)
    income_df = stock.financials
    income_statement[symbol] = income_df
    time.sleep(1.5)
    
print(income_statement.get("AAPL", "No data for AAPL"))
