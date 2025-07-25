import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Load S&P 500 companies
sp500_list = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = sp500_list[0]
sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=False)
symbol_list = sp500["Symbol"].unique().tolist()

# User input
symbols_input = input("Enter up to 10 ticker symbols, separated by commas: ")
user_symbols = [s.strip().upper() for s in symbols_input.split(",")][:10]

# Markers
markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X', 'h', '+']

# Plotting
plt.figure(figsize=(10, 6))

for i, symb in enumerate(user_symbols):
    if symb in symbol_list:
        data = yf.Ticker(symb)
        price = data.info.get("regularMarketPrice")
        change = data.info.get("regularMarketChangePercent")
        if price is not None and change is not None:
            plt.scatter(price, change, marker=markers[i % len(markers)], label=symb)
    else:
        print(f"Symbol '{symb}' is not in the S&P 500 list. Skipped.")


plt.xlabel("Regular Market Price")
plt.ylabel("Regular Market Change Percent")
plt.title("Selected S&P 500 Stocks: Price vs % Change")

plt.subplots_adjust(right=0.75)
plt.legend(
    title="Ticker Symbols",
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    borderaxespad=0.
)

plt.tight_layout()
plt.show()


# layerone = completion.choices[0].message.content.strip().split()

# clean_symbols = [s.strip().replace('$', '').replace(',', '').upper() for s in layerone[:5]]

# symbols = yf.Tickers(clean_symbols)
# count = 0
# for symbol in clean_symbols:
#     ticker = symbols.tickers[symbol]
#     recs = ticker.recommendations
#     hist = ticker.history(period="5d")
#     print(symbol, hist, "\n", recs, "\n")

