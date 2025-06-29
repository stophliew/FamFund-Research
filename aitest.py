from openai import OpenAI
import realtimedata

client = OpenAI(
    api_key="sk-proj-Wxiayo3dxvvPv9_0HCu5B7IQbsEX7-Qzt3VWy9-"
    "s2HXUQEG4a8n4ajuI96zm46KG3vCfG3MmhuT3BlbkFJGP0u"
    "ZHGm9L2u9NN6S_nf7UTC7dEGNqjQ"
    "r3pSbXyIbGokvYOGbVRPqFOQpQGRmG2VOdn-pVpHcA"
)

earningsdata = realtimedata.earnings()
market_statusdata = realtimedata.market_status()
earnings_str = str(earningsdata)
market_status_str = str(market_statusdata)

prompt = (
    f"You are a financial advisor. You are given current up-to-date data:\n\n"
    f"Earnings data:\n"
    f"Market status data:\n{market_status_str}\n"
    "You are in charge of guiding a group of clients through"
    "their investments. "
    "Most of them are new to investing, so be clear and concise "
    "in your explanations. "
    "Consider the stock market, financial news, and current geopolitical "
    "tensions (especially in tech). "
    "Community: Which five companies should I invest in right now?"
)


completion = client.chat.completions.create(
    model="gpt-4.1-nano-2025-04-14",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(completion.choices[0].message.content)
