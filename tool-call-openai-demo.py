from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv(override=True)

client = OpenAI()

def get_max_mustermanns_nickname():
    return "Maexchen"

max_mustermanns_nickname_json = {
    "name": "get_max_mustermanns_nickname",
    "description": "Use this tool to get Max Mustermanns nickname",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": max_mustermanns_nickname_json}]

messages=[{"role": "user", "content": "What is Max Mustermanns nickname?"}]

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages,
    tools=tools,
    temperature=1
)

print(json.dumps(response.model_dump(), indent=2))