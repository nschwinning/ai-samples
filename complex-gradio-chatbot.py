from anthropic import AnthropicFoundry
from openai import AzureOpenAI
from dotenv import load_dotenv
import gradio as gr
from pydantic import BaseModel

load_dotenv(override=True)

anthropic_client = AnthropicFoundry()
open_ai_client = AzureOpenAI(
    api_version="2024-08-01-preview"
)

system_prompt = """
    You are a neoliberal economist. All arguments, explanations, and conclusions must be framed strictly from a neoliberal economic perspective, 
    emphasizing market efficiency, deregulation, competition, and limited government intervention. Do not step out of this role at any point.
    """

evaluator_system_prompt = """
    You are an evaluator that decides whether a response to a question is acceptable. 
    You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. 
    The Agent is playing the role of a neoliberal economist. 
    The Agent has been instructed to be professional and engaging and to not step out of the role
    With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback.
    """

def evaluator_user_prompt(reply, message, history):
    user_prompt = f"Here's the conversation between the User and the Agent: \n\n{history}\n\n"
    user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
    user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
    user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
    return user_prompt

#
# def chat(message, history):
#     messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
#     response = open_ai_client.chat.completions.create(model="gpt-5.1-chat", messages=messages)
#     return response.choices[0].message.content

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

def evaluate(reply, message, history) -> Evaluation:

    messages = [{"role": "system", "content": evaluator_system_prompt}] + [{"role": "user", "content": evaluator_user_prompt(reply, message, history)}]
    response = open_ai_client.chat.completions.parse(model="gpt-5.1-chat", messages=messages, response_format=Evaluation)
    return response.choices[0].message.parsed

def rerun(reply, message, history, feedback):
    updated_system_prompt = system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
    updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
    updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
    #messages = history + [{"role": "user", "content": message}]
    messages = []

    # History aus Gradio → Anthropic-Format
    for history_message in history:
        messages.append({"role": history_message['role'], "content": history_message['content'][0]['text']})

    # Neue User-Nachricht anhängen
    messages.append({"role": "user", "content": message})
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        system=system_prompt,
        messages=messages,
        max_tokens=500
    )
    return response.content[0].text


def chat(message, history):
    messages = []

    # History aus Gradio → Anthropic-Format
    for history_message in history:
        messages.append({"role": history_message['role'], "content": history_message['content'][0]['text']})

    # Neue User-Nachricht anhängen
    messages.append({"role": "user", "content": message})
    #messages = history + [{"role": "user", "content": message}]
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        system=system_prompt,
        messages=messages,
        max_tokens=500
    )
    reply = response.content[0].text

    evaluation = evaluate(reply, message, history)

    if evaluation.is_acceptable:
        print("Passed evaluation - returning reply")
    else:
        print("Failed evaluation - retrying")
        print(evaluation.feedback)
        reply = rerun(reply, message, history, evaluation.feedback)
    return reply

gr.ChatInterface(fn=chat).launch()
