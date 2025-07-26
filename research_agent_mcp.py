industry_sector = None
from agents import *
import asyncio

# Multi-Context Protocol
message_queue = asyncio.Queue()

def create_message(sender, receiver, content):
    return {"sender": sender, "receiver": receiver, "content": content}


# Mixture of Experts Concept
quantitative_researcher = Agent(name="Quantitative Researcher",
            model="gpt-4.1-nano-2025-04-14",
            tools=[WebSearchTool()],
            instructions="You are a quantiative researcher with extensive knowledge in finance and stocks",
            )

market_analyst = Agent(name="Market Analyst", 
            model="gpt-4.1-nano-2025-04-14",
            tools=[WebSearchTool()],
            instructions="Analyze market conditions, trends, and sentiment with precision. Use web data to support insights."
            )

inside_movement = Agent(name="Insider Movement Tracker", 
            model="gpt-4.1-nano-2025-04-14",
            tools=[WebSearchTool()],
            instructions="Focus on tracking and analyzing insider trades, SEC filings, and executive movements."
            )


def create_message(sender, receiver, content):
    return {
        "sender": sender,
        "receiver": receiver,
        "content": content
    }
def search(query):
    import asyncio
    async def run_and_collect():
        tasks = await run_all()
        return [task.final_output for task in tasks]
    return asyncio.run(run_and_collect())

async def agent_task(agent, prompt, send_to=None, send_msg=None):
    result = await Runner.run(agent, prompt)
    if send_to and send_msg:
        await message_queue.put(create_message(agent.name, send_to, send_msg))
    await asyncio.sleep(0.1)
    received_msgs = []
    new_queue = asyncio.Queue()
    while not message_queue.empty():
        msg = await message_queue.get()
        if msg["receiver"] == agent.name:
            print(f"{agent.name} received message from {msg['sender']}: {msg['content']}")
            received_msgs.append(msg)
        else:
            await new_queue.put(msg)
    while not new_queue.empty():
        await message_queue.put(await new_queue.get())
    return result

async def run_all():
    tasks = await asyncio.gather(
        agent_task(
            quantitative_researcher,
            f"Analyze current trends in the given sector {industry_sector}",
            send_to="Market Analyst",
            send_msg="Check my findings for possible market sentiment changes. Concisely"
        ),
        agent_task(
            market_analyst,
            f"Analyze current trends in the given sector {industry_sector} ",
            send_to="Insider Movement Tracker",
            send_msg="Let me know about any big insider trades in the given industry sector. Concisely"
        ),
        agent_task(
            inside_movement,
            f"Analyze current trends in the given industry sector {industry_sector}",
            send_to="Quantitative Researcher",
            send_msg="Reporting significant insider buy/sell events. Concisely"
        ),
    )
    return tasks

if __name__ == "__main__":
    results = asyncio.run(run_all())
    for res in results:
        print(res.final_output)