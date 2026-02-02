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

finish_reason = response.choices[0].finish_reason

if finish_reason == "tool_calls":
    message = response.choices[0].message
    tool_calls = message.tool_calls
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Calling tool: {tool_name} with arguments {arguments}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        messages.append(message)
        messages.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            tools=tools,
            temperature=1
        )
        print(response.choices[0].message.content)