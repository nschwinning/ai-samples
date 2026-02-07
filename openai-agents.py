import asyncio
from agents import Agent, Runner, trace
from dotenv import load_dotenv

async def simple_agent():
    agent = Agent(
        name="Jokester",
        instructions="You are a funny agent and a joke teller."
    )

    with trace("Telling a joke"):
        result = await Runner.run(
            agent,
            "Tell a joke about Autonomous AI Agents"
        )

        print(result.final_output)

async def multi_agent():
    agent_1 = Agent(
        name="Agent 1",
        instructions="You work in a bank and give financial advice to people.",
        model="gpt-5-mini"
    )

    agent_2 = Agent(
        name="Agent 2",
        instructions="You have a background in math and finance and know the stock market and its products well.",
        model="gpt-5-mini"
    )

    message = "Give me a strategy how I should invest my money now seeking for financial independence after I retire in 30 years."

    with trace("Parallel financial advice"):
        results = await asyncio.gather(
            Runner.run(agent_1, message),
            Runner.run(agent_2, message),
        )

        agent_outputs = [
            ("Agent 1", results[0].final_output),
            ("Agent 2", results[1].final_output),
        ]

        sections = [f"Strategy from {name}:\n\n{text}" for name, text in agent_outputs]
        strategies = "\n\n---\n\n".join(sections)
        print(strategies)

        strategy_picker = Agent(
            name="Strategy Picker",
            instructions="You evaluate financial strategies in your daily work. Pick the best strategy for a customer that seeks for financial independence in retirement and explain why.",
            model="gpt-5-mini"
        )

        result = await Runner.run(strategy_picker, strategies)

        print(f"Best strategy:\n{result.final_output}")

async def main():
    load_dotenv(override=True)

    await multi_agent()

if __name__ == "__main__":
    asyncio.run(main())
