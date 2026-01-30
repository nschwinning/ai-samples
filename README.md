
This repository contains minimal, runnable Python examples showing how to connect to Azure AI services exposed via Azure Foundry using official SDKs. It includes:

- Anthropic via Azure Foundry using the `anthropic` SDK (`AnthropicFoundry` client)
- Azure OpenAI via the `openai` SDK (`AzureOpenAI` client)
- Two Gradio chat demos built on top of Anthropic via Azure Foundry


## Prerequisites

- Python 3.12 or newer
- An Azure Foundry deployment with access to the respective models
- API keys and endpoints (see Environment variables)
- Optional: `uv` (recommended) or `pip` for dependency management


## Environment variables

The examples read credentials from a local `.env` file using `python-dotenv`. Create a `.env` file in the project root with the following keys as needed:

Required for Anthropic via Azure Foundry (`AnthropicFoundry` client):

- `ANTHROPIC_FOUNDRY_API_KEY` — API key for the Azure Foundry resource that exposes Anthropic models
- `ANTHROPIC_FOUNDRY_RESOURCE` — Name of the Azure Foundry resource (e.g., `my-ai-service-01`)

Required for Azure OpenAI (`AzureOpenAI` client):

- `AZURE_OPENAI_API_KEY` — API key for the Azure OpenAI resource
- `AZURE_OPENAI_ENDPOINT` — Endpoint URL for the Azure OpenAI resource (e.g., `https://<resource-name>.services.ai.azure.com`)

Example `.env`:

```
ANTHROPIC_FOUNDRY_API_KEY=...your_anthropic_foundry_key...
ANTHROPIC_FOUNDRY_RESOURCE=your-foundry-resource-name

AZURE_OPENAI_API_KEY=...your_azure_openai_key...
AZURE_OPENAI_ENDPOINT=https://your-foundry-resource-name.services.ai.azure.com
```

Note: Do not commit real secrets. The `.gitignore` should already exclude `.env`.


## Install dependencies

Using uv (recommended):

```
uv sync
```

Or using pip:

```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r <(python - <<'PY'
import tomllib, sys
from pathlib import Path
data = tomllib.loads(Path('pyproject.toml').read_text())
for dep in data['project']['dependencies']:
    print(dep)
PY
)
```


## Examples

### 1) Anthropic via Azure Foundry (CLI demo)

File: `azure-anthropic-demo.py`

What it does:
- Loads `.env`
- Instantiates `AnthropicFoundry()`
- Sends a user message and prints the model reply from `claude-sonnet-4-5`

Run:

```
uv run python azure-anthropic-demo.py
# or
python azure-anthropic-demo.py
```

Environment required: `ANTHROPIC_FOUNDRY_API_KEY`, `ANTHROPIC_FOUNDRY_RESOURCE`


### 2) Azure OpenAI (CLI demo)

File: `azure-openai-demo.py`

What it does:
- Loads `.env`
- Instantiates `AzureOpenAI(api_version="2024-02-15-preview")`
- Calls `chat.completions.create` with `model="gpt-5.1-chat"`

Run:

```
uv run python azure-openai-demo.py
# or
python azure-openai-demo.py
```

Environment required: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`


### 3) Simple Gradio Chatbot (Anthropic via Azure Foundry)

File: `simple-gradio-chatbot.py`

What it does:
- Loads `.env`
- Uses `AnthropicFoundry()` to chat with `claude-sonnet-4-5`
- Presents a minimal Gradio `ChatInterface`

Run and open the provided local URL in your browser:

```
uv run python simple-gradio-chatbot.py
# or
python simple-gradio-chatbot.py
```

Environment required: `ANTHROPIC_FOUNDRY_API_KEY`, `ANTHROPIC_FOUNDRY_RESOURCE`


### 4) Complex Gradio Chatbot with Auto-Evaluation

File: `complex-gradio-chatbot.py`

What it does:
- Loads `.env`
- Uses `AnthropicFoundry()` for the main assistant (model `claude-sonnet-4-5`)
- Uses `AzureOpenAI` with `response_format` parsing to evaluate responses against a strict persona/system prompt
- If a reply is rejected by the evaluator, it regenerates a reply with additional guidance

Run:

```
uv run python complex-gradio-chatbot.py
# or
python complex-gradio-chatbot.py
```

Environment required:
- Anthropic via Foundry: `ANTHROPIC_FOUNDRY_API_KEY`, `ANTHROPIC_FOUNDRY_RESOURCE`
- Azure OpenAI: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`


## Notes

- All scripts call `load_dotenv(override=True)` so `.env` values take precedence in your shell.
- Model names are configured inline. Update to available models in your Azure Foundry/region if needed.
- If you encounter authentication errors, double-check the resource name and endpoint URL spelling and that your key has access.


## Useful links

- Anthropic Python SDK: https://github.com/anthropics/anthropic-sdk-python
- Azure OpenAI with OpenAI SDK (Azure OpenAI compatibility): https://learn.microsoft.com/azure/ai-services/openai/how-to/sdk?pivots=programming-language-python
- Gradio: https://www.gradio.app/

