import base_agent
industry_sector = input("Community Focus: ").strip()
base_agent.industry_sector = industry_sector
from openai import OpenAI
client = OpenAI()

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        break
    if "research" in user_input.lower():
        context_chunks = base_agent.search(user_input)
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
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are Athena, an expert investment consultant, with deep knowledge in investing and finance"},
            {"role": "user", "content": f"{user_input}\n\nContext:\n{context}"}
        ]
    )
    print("Athena:", response.choices[0].message.content.strip())