import json
import requests
import yfinance as yf
import pandas as pd
from openai import OpenAI


client = OpenAI()


# Testing User Source
investments = input("Enter your investments in their respective stock tickers (separated by commas): ")
invested = [ticker.strip().upper() for ticker in investments.split(",") if ticker.strip() != ""]

company_info = {}
# Historical Data Retrieval 
for companies in invested:
    # Information Package
    dat = yf.Ticker(companies)
    recs = dat.get_recommendations()
    est = dat.get_growth_estimates()
    ins_p = dat.get_insider_purchases()
    info = dat.info
    company_info[companies] = {
        "recommendations": recs.to_dict(),
        "growth_estimates": est.to_dict(),
        "insider_purchases": ins_p.to_dict(),
        "beta": info.get("beta"),
        "pe_ratio": info.get("trailingPE"),
        "eps": info.get("trailingEps"),
        "market_cap": info.get("marketCap"),
    }

print(company_info)

benchmark_tickers = ["^GSPC", "QQQ", "GLD"]
benchmark_data = {
    ticker: yf.Ticker(ticker).history(period="1y")['Close'] for ticker in benchmark_tickers
}
portfolio_history = {
    ticker: yf.Ticker(ticker).history(period="1y")['Close'] for ticker in invested
}

# Comparison 
snp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
snp500['Symbol'] = snp500['Symbol'].str.replace("-",",")
symb_list = snp500["Symbol"].unique().tolist()

input_prompt = f"""
Portfolio: {invested}
Data: {json.dumps(company_info)}
Task:
1. Assign a health score out of 100 based on:
   - Historical returns vs S&P 500, QQQ, GLD
   - Insider buying/selling activity
   - Analyst recommendations
   - Growth outlook
   - Geopolitical and economic context
2. Highlight strengths and red flags.
3. Include final recommendation (Hold/Sell/Buy more).
"""

response = client.responses.create(
    model="gpt-4.1",
    tools=[{
        "type": "web_search_preview",
        "search_context_size": "low",
    }],
    input=input_prompt
)

print("\n" + response.output_text)
