from agents import *
import asyncio

# Mixture of Experts Concept
quantitative_researcher = Agent(name="Quantitative Researcher",
            model="gpt-4o-mini-2024-07-18",
            tools=[WebSearchTool()],
            instructions="You are a quantiative researcher with extensive knowledge in finance and stocks",
            )

market_analyst = Agent(name="Market Analyst", 
            model="gpt-4o-mini-2024-07-18",
            tools=[WebSearchTool()],
            instructions="Analyze market conditions, trends, and sentiment with precision. Use web data to support insights."
            )

inside_movement = Agent(name="Insider Movement Tracker", 
            model="gpt-4o-mini-2024-07-18",
            tools=[WebSearchTool()],
            instructions="Focus on tracking and analyzing insider trades, SEC filings, and executive movements."
            )

async def run_all():
    tasks = await asyncio.gather(
        Runner.run(quantitative_researcher, "Analyze current trends in the semiconductor and how it might affect NVDA"),
        Runner.run(market_analyst, "Analyze current trends in the semiconductor"),
        Runner.run(inside_movement, "Analyze current trends in the semiconductor"),
    )
    return tasks


if __name__ == "__main__":
    results = asyncio.run(run_all())
    for res in results:
        print(res.final_output)