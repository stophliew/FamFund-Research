import requests
import json
from openai import OpenAI

ALPHA_KEY = "DXL7K0GZEMR3P8RZ"
client = OpenAI(
    api_key="sk-proj-Wxiayo3dxvvPv9_0HCu5B7IQbsEX7-Qzt3VWy9-"
    "s2HXUQEG4a8n4ajuI96zm46KG3vCfG3MmhuT3BlbkFJGP0u"
    "ZHGm9L2u9NN6S_nf7UTC7dEGNqjQ"
    "r3pSbXyIbGokvYOGbVRPqFOQpQGRmG2VOdn-pVpHcA"
)


def feedback():
    userfocus = input("Prompt your community's focus, specify which market and how much you currently have: \n> ")
    return userfocus


def betawebsearch():
    userinput = input("Prompt FamFund's agent to conduct research on a topic:\n> ")
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You're a financial research agent. "
            "Use the following query to summarize information as if from the web."},
            {"role": "user", "content": userinput}
        ]
    )
    return response.choices[0].message.content.strip()


def get_market_data():
    news_url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={ALPHA_KEY}"
    insider_url = f"https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey={ALPHA_KEY}"
    gainers_url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={ALPHA_KEY}"

    news = requests.get(news_url).json()
    insider = requests.get(insider_url).json()
    gainers = requests.get(gainers_url).json()

    return news, insider, gainers


def create_prompt(news, insider, gainers, websearch, feedback):
    prompt = (
        "You are an AI investment assistant. Do not contradict yourself\n"
        f"Focus on this topics: {feedback}\n"
        "Include a short description on recent insider trading\n"
        "Suggest the best industry/sector to invest at the current time\n"
        "Please read this market data and give:\n"
        "- Overall market condition\n"
        "- 3 good stocks to consider\n"
        "- 2 stocks to avoid based on the requested sector\n"
        "- A health score from 0 to 100\n\n"
        f"News: {json.dumps(news)[:3000]}\n\n"
        f"Insider Trading: {json.dumps(insider)[:1500]}\n\n"
        f"Gainers and Losers: {json.dumps(gainers)[:1000]}\n"
        f"User context: {json.dumps(websearch)}\n"
    )
    return prompt


def get_investment_summary(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def main(websearch, feedback):
    news, insider, gainers = get_market_data()
    prompt = create_prompt(news, insider, gainers, websearch, feedback)
    summary = get_investment_summary(prompt)
    print(f"=== Daily Investment Report ===\n{summary}")


main(feedback=feedback(), websearch=betawebsearch())
