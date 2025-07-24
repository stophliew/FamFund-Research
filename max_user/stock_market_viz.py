import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Load S&P 500 companies
sp500_list = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = sp500_list[0]
sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=False)
symbol_list = sp500["Symbol"].unique().tolist()


symbols_input = input("Enter up to 10 ticker symbols, separated by commas: ")
user_symbols = [s.strip().upper() for s in symbols_input.split(",")][:10]

markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X', 'h', '+']

for i, symb in enumerate(user_symbols):
    if symb in symbol_list:
        data = yf.Ticker(symb)
        price = data.info.get("regularMarketPrice")
        change = data.info.get("regularMarketChangePercent")
        if price is not None and change is not None:
            plt.scatter(price, change, marker=markers[i % len(markers)], label=symb)
    else:
        print(f"Symbol '{symb}' is not in the S&P 500 list. Skipped.")

plt.xlabel("regularMarketPrice")
plt.ylabel("regularMarketChangePercent")
plt.legend(title="Ticker Symbols", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
