import asyncio
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

# Disable tracing since we're using Azure OpenAI
set_tracing_disabled(disabled=True)

deployment = "gpt-5.1-chat"

async def main():
    load_dotenv(override=True)

    client = AsyncAzureOpenAI(
        api_version="2024-02-15-preview"
    )

    agent = Agent(
        name="Jokester",
        instructions="You are a funny agent and a joke teller.",
        model=OpenAIChatCompletionsModel(
            model=deployment,
            openai_client=client
        )
    )

    with trace("Telling a joke"):
        result = await Runner.run(
            agent,
            "Tell a joke about Autonomous AI Agents"
        )

        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
