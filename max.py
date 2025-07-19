import yfinance as yf
from openai import OpenAI
import requests
import json
import os

# data pipeline

# tech news
url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=DXL7K0GZEMR3P8RZ"
r = requests.get(url)
news = r.json()

# insider trading
url = "https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=DXL7K0GZEMR3P8RZ"
r = requests.get(url)
insidertrading = r.json()

# top gain and losers
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

# Add Perplexity Sonar API integration
SONAR_API_KEY = os.getenv("SONAR_API_KEY") or "YOUR_SONAR_API_KEY"
SONAR_API_URL = "https://openrouter.ai/api/v1/chat/completions"
SONAR_MODEL = "perplexity/sonar"

def sonar_search(query):
    headers = {
        "Authorization": f"Bearer {SONAR_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": SONAR_MODEL,
        "messages": [
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(SONAR_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Sonar API error: {response.status_code} {response.text}"

# Example: Use Sonar to get relevant search results for the investment prompt
user_query = "What are the most relevant financial news and trends for NASDAQ investments this week?"
sonar_results = sonar_search(user_query)

prompt = (
    "You're an investment consultant, advising a community on what investments to make"
    "You are a RAG-agent and have external resources from the datasets provided"
    "Please output five companies and their NASDAQ symbols based on the following criteria"
    "Income statement, current stock price, geopolitical issues, and insider trading activities"
    f"{news},{insidertrading}, {gandl} "
    f"\nRelevant web search: {sonar_results}\n"
    "Strictly limit your output to be five stock symbols in a single line and make sure there is nothing else"
)

completion = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
print(completion.choices[0].message.content)

# layerone = completion.choices[0].message.content.strip().split()

# clean_symbols = [s.strip().replace('$', '').replace(',', '').upper() for s in layerone[:5]]

# symbols = yf.Tickers(clean_symbols)
# count = 0
# for symbol in clean_symbols:
#     ticker = symbols.tickers[symbol]
#     recs = ticker.recommendations
#     hist = ticker.history(period="5d")
#     print(symbol, hist, "\n", recs, "\n")

