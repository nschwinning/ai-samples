from anthropic import AnthropicFoundry
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)

client = AnthropicFoundry()

def query_anthropic(text, history):
    messages = []

    # History aus Gradio → Anthropic-Format
    for history_message in history:
        messages.append({"role": history_message['role'], "content": history_message['content'][0]['text']})

    # Neue User-Nachricht anhängen
    messages.append({"role": "user", "content": text})

    response = client.messages.create(
        model="claude-sonnet-4-5",
        messages=messages,
        max_tokens=500
    )

    return response.content[0].text


# demo = gr.Interface(
#     fn=query_anthropic,
#     inputs=["text"],
#     outputs=[gr.Textbox(label="answer", lines=10)],
#     api_name="predict"
# )

demo=gr.ChatInterface(
    fn=query_anthropic,
).launch()

demo.launch()
