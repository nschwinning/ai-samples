# Azure Open AI Demo, AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set

from openai import AzureOpenAI

from dotenv import load_dotenv

load_dotenv(override=True)

client = AzureOpenAI(
    api_version="2024-02-15-preview"
)

messages=[{"role": "user", "content": "Schreibe mir eine kurze Zusammenfassung von Azure Foundry."}]

response = client.chat.completions.create(
    model="gpt-5.1-chat",
    messages=messages,
    temperature=1
)

print(response.choices[0].message.content)
