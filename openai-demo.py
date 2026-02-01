from openai import OpenAI

from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

messages=[{"role": "user", "content": "Schreibe mir eine kurze Zusammenfassung von Azure Foundry."}]

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages,
    temperature=1
)

print(response.choices[0].message.content)
