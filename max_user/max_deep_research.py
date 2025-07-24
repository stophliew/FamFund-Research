import requests
import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-Wxiayo3dxvvPv9_0HCu5B7IQbsEX7-Qzt3VWy9-"
    "s2HXUQEG4a8n4ajuI96zm46KG3vCfG3MmhuT3BlbkFJGP0u"
    "ZHGm9L2u9NN6S_nf7UTC7dEGNqjQ"
    "r3pSbXyIbGokvYOGbVRPqFOQpQGRmG2VOdn-pVpHcA"
)


completion = client.chat.completions.create(
    model="gpt-4.1-2025-04-14",
    messages=[
        {"role": "user", "content": ""}
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

