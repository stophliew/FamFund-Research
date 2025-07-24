import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-Wxiayo3dxvvPv9_0HCu5B7IQbsEX7-Qzt3VWy9-"
    "s2HXUQEG4a8n4ajuI96zm46KG3vCfG3MmhuT3BlbkFJGP0u"
    "ZHGm9L2u9NN6S_nf7UTC7dEGNqjQ"
    "r3pSbXyIbGokvYOGbVRPqFOQpQGRmG2VOdn-pVpHcA"
)

def get_user_focus():
    return input("Prompt your community's focus, specify which market: \n> ")

def get_market_research(user_interest):
    response = client.responses.create(
        model="o4-mini-2025-04-16",
        tools=[{"type": "web_search_preview"}],
        input=f"Conduct deep research based on the user's interest, include insider trading on the industry specified {user_interest}"
    )
    return response.output_text

def generate_investment_report(market_data, user_focus):
    prompt = (
        f"You are an AI investment assistant focused on: {user_focus}\n"
        "Provide:\n"
        "- Overall market condition\n"
        "- 10 good stocks to consider\n"
        "- 10 stocks to avoid\n"
        "- Recent insider trading insights\n"
        "- Best investment sector recommendation\n"
        "- Market health score (0-100)\n\n"
        f"Market Data: {json.dumps(market_data)[:3000]}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def main():
    user_focus = get_user_focus()
    market_data = get_market_research(user_focus)
    report = generate_investment_report(market_data, user_focus)
    print(f"=== Investment Report ===\n{report}")

if __name__ == "__main__":
    main()