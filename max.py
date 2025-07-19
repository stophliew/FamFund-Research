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

# Add OpenAI websearch integration (from base.py)
def openai_websearch(query):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You're a financial research agent. Use the following query to summarize information as if from the web."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()

# Step 1: Gather external data from Sonar and OpenAI websearch
user_query = "What are the most relevant financial news and trends for NASDAQ investments this week?"
sonar_results = sonar_search(user_query)
openai_web_results = openai_websearch(user_query)

# Step 2: LLM (funnel) - Generate investment recommendations
llm_prompt = (
    "You're an investment consultant, advising a community on what investments to make. "
    "You are a RAG-agent and have external resources from the datasets provided. "
    "Please output five companies and their NASDAQ symbols based on the following criteria: "
    "Income statement, current stock price, geopolitical issues, and insider trading activities. "
    f"Market data: {news}, {insidertrading}, {gandl}. "
    f"\nRelevant web search (Sonar): {sonar_results}\n"
    f"Relevant web search (OpenAI): {openai_web_results}\n"
    "Strictly limit your output to be five stock symbols in a single line and make sure there is nothing else."
)
llm_completion = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14",
    messages=[{"role": "user", "content": llm_prompt}]
)
llm_output = llm_completion.choices[0].message.content.strip()

# Step 3: LRM (evaluator) - Evaluate LLM output and make final decision
lrm_prompt = (
    "You are a financial reasoning agent. Evaluate the following investment recommendations for accuracy, relevance, and risk, using all the provided external data. "
    "If the recommendations are sound, output the five stock symbols in a single line. If not, suggest corrections. "
    f"\nLLM output: {llm_output}\n"
    f"Market data: {news}, {insidertrading}, {gandl}. "
    f"Web search (Sonar): {sonar_results}\n"
    f"Web search (OpenAI): {openai_web_results}\n"
)
lrm_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": lrm_prompt}]
)
final_decision = lrm_completion.choices[0].message.content.strip()

print("=== MAX Investment Recommendation ===")
print(final_decision)

