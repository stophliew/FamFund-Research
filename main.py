import yfinance as yf
from openai import OpenAI

#data pipeline

#tech news
url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=DXL7K0GZEMR3P8RZ"
r = requests.get(url)
news = r.json()

#insider trading
url = "https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=DXL7K0GZEMR3P8RZ" 
r = requests.get(url)
insidertrading = r.json()

#top gain and losers
url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=DXL7K0GZEMR3P8RZ"
r = requests.get(url)
gandl = r.json()

sources = [news, insidertrading, gandl]
combined_data = ""
for i in sources:
    combined_data += json.dumps(i) + "\n"


client = OpenAI(
    api_key="sk-proj-Wxiayo3dxvvPv9_0HCu5B7IQbsEX7-Qzt3VWy9-"
    "s2HXUQEG4a8n4ajuI96zm46KG3vCfG3MmhuT3BlbkFJGP0u"
    "ZHGm9L2u9NN6S_nf7UTC7dEGNqjQ"
    "r3pSbXyIbGokvYOGbVRPqFOQpQGRmG2VOdn-pVpHcA"
)

prompt = (
    "You're an investment consultant, advising a community on what investments to make" 
    "You are a RAG-agent and have external resources from the datasets provided" 
    "Please output five companies and their NASDAQ symbols based on the following criteria" 
    "Income statement, current stock price, geopolitical issues, and insider trading activities" 
    f"{news},{insidertrading}, {gandl} "
    "Strictly limit your output to be five stock symbols in a single line and make sure there is nothing else" 
)

completion = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

layerone = completion.choices[0].message.content.strip().split()

clean_symbols = [s.strip().replace('$', '').replace(',', '').upper() for s in layerone[:5]]

symbols = yf.Tickers(clean_symbols)
count = 0
for symbol in clean_symbols:
    ticker = symbols.tickers[symbol]
    recs = ticker.recommendations
    hist = ticker.history(period="5d")
    print(symbol, hist, "\n", recs, "\n")

