# Azure Anthropic AI Demo, ANTHROPIC_FOUNDRY_API_KEY and ANTHROPIC_FOUNDRY_RESOURCE must be set

from anthropic import AnthropicFoundry
from dotenv import load_dotenv

load_dotenv(override=True)

client = AnthropicFoundry()

messages=[{"role": "user", "content": "Schreibe mir eine kurze Zusammenfassung von Azure Foundry."}]

# 3) Anfrage an das Modell
response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=messages,
    max_tokens=500
)

print(response.content[0].text)
