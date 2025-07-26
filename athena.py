import research_agent_mcp as research_agent_mcp 
industry_sector = input("Community Focus: ").strip()
research_agent_mcp.industry_sector = industry_sector
from openai import OpenAI
client = OpenAI()


while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    if "research" in user_input.lower():
        context_chunks = research_agent_mcp.search(user_input)
        if context_chunks:
            if isinstance(context_chunks, list):
                context = "\n\n".join(context_chunks)[:1000]
            else:
                context = str(context_chunks)[:1000]
        else:
            context = "(No relevant research results.)"
    else:
        context = "(No research triggered; keyword 'research' not found.)"

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "You are Athena, an expert investment consultant, "
            "with deep knowledge in investing and finance"
            "Start off every chat with a warm welcoming message, include in the sentence that you're FamFund's premier consultant agent"
            "Guidelines: "
            "Never engage in irrevelent interactions, keep everything related to"
            "Finance, Stock-Market, Investment, and Business"
            "Absolutely Nothing Else: Response with I'm sorry I cannot help you with that"},
            {"role": "user", "content": f"{user_input}\n\nContext:\n{context}"}
        ]
    )
    print("Athena:", response.choices[0].message.content.strip())
