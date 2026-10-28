# Nova AI Chatbot — AI Class Lab Project

A general-purpose conversational AI web app built with Python, Streamlit, and the Groq API.

## Features

- Natural-language answers from a hosted language model
- Conversation context for follow-up questions (recent messages are sent with each request)
- ChatGPT-style message interface
- Example prompts, clear-chat control, and JSON conversation export
- API key read from Streamlit secrets or an environment variable
- Friendly handling for authentication, rate-limit, connection, and API errors
- Configurable model ID through the sidebar or `GROQ_MODEL` environment variable

> This is an API-backed chatbot, not a model trained from scratch. Availability and free usage limits depend on the provider, account, and model. Check your Groq console before relying on a model ID.

## Requirements

- Windows 10/11
- Python 3.10 or newer (a stable supported Python version is recommended)
- Internet connection
- A Groq account and API key: https://console.groq.com/keys

## Windows setup (PowerShell)

Open PowerShell and run:

```powershell
mkdir C:\AIChatbot
cd C:\AIChatbot
```

Extract this project ZIP into `C:\AIChatbot` (or open PowerShell in the extracted project folder). Then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, skip activation and use the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configure the API key securely

1. Create a key at https://console.groq.com/keys.
2. In the project folder, open `.streamlit`.
3. Copy `secrets.toml.example` and name the copy `secrets.toml`.
4. Open `secrets.toml` and replace the placeholder with your key:

```toml
GROQ_API_KEY = "your_real_key_here"
```

Alternative: set an environment variable in the same PowerShell window:

```powershell
$env:GROQ_API_KEY = "your_real_key_here"
```

Do not put the real key in `app.py`, screenshots, reports, public repositories, or messages. The included `.gitignore` excludes `.streamlit/secrets.toml`.

## Run the chatbot

From the project folder, with the virtual environment active:

```powershell
streamlit run app.py
```

If the `streamlit` command is not found:

```powershell
python -m streamlit run app.py
```

Streamlit should open the local app in your browser, usually at `http://localhost:8501`. Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

## Configure a different model

The default is `llama-3.3-70b-versatile`, based on the provider's published quickstart at the time this project was prepared. Model availability can change. If it is unavailable, select a currently supported model ID in the sidebar or set `GROQ_MODEL` before launch:

```powershell
$env:GROQ_MODEL = "your_available_model_id"
python -m streamlit run app.py
```

## Test checklist

1. Ask `What is artificial intelligence?` — expect a relevant explanation.
2. Ask `Explain BFS` and then `Compare it with DFS` — the second response should use recent context.
3. Ask for a simple Python program — expect code and explanation.
4. Click an example prompt — it should be submitted to the model.
5. Click **Export conversation (JSON)** — a JSON file should download.
6. Click **Clear conversation** — the visible conversation should reset.
7. Temporarily remove the key from `secrets.toml` and restart — expect a helpful missing-key message. Restore it afterward.
8. Try an invalid model ID — expect an API error message rather than an unhandled crash.
9. Test an invalid API key only if needed; do not expose or share your real key.

## Troubleshooting

- **`py` not recognized:** install Python from https://www.python.org/downloads/ and enable the option to add Python to PATH, then reopen PowerShell.
- **Activation is blocked:** use the full `.venv\Scripts\python.exe` commands above instead of changing system execution policy.
- **API key missing:** check `.streamlit/secrets.toml` spelling and TOML quotes, then restart Streamlit.
- **401/authentication error:** create or copy a valid key and update the secrets file.
- **429/rate limit:** wait and retry; review your account's current limits.
- **Model not found/decommissioned:** choose a model ID currently listed in the provider console/docs.
- **Package import error:** activate the environment and run `python -m pip install -r requirements.txt`.

## Project structure

```text
ai_class_lab_chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
├── report.md
└── tests/
    └── manual_test_plan.md
```

## Limitations

- Requires internet access and a valid provider API key.
- The free tier is subject to change and rate limits; it is not unlimited.
- Model responses can be wrong or outdated. Verify important claims.
- Conversation history is stored in Streamlit session state and is not a persistent database; it normally resets when the session is reset.
- No authentication, database-backed history, web search, file upload, or voice features are included in this starter project.

## Suggested future enhancements

Persistent accounts and chat history, file/document question answering (RAG), web search, speech input/output, response streaming, and deployment on Streamlit Community Cloud with secrets configured in the deployment settings.
