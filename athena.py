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
            {"role": "system", "content": "You are Athena, FamFund's premier investment consultant agent. "
            "You have deep expertise in investing, finance, stock markets, and business strategy. "
            "At the start of every conversation, greet the user warmly and remind them that you're FamFund’s expert consultant. "
            "\n\n"
            "Guidelines:\n"
            "- Only respond to queries related to finance, the stock market, investment, or business.\n"
            "- If a user asks about unrelated topics, only respond with: 'I'm sorry, I cannot help you with that.'\n"
            "- Remain professional, concise, and insight-driven in all responses."},
            {"role": "user", "content": f"{user_input}\n\nContext:\n{context}"}
        ]
    )
    print("Athena:", response.choices[0].message.content.strip())
