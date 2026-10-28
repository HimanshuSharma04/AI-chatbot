import json
import os
from datetime import datetime

import streamlit as st
from groq import Groq
from groq import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError

APP_TITLE = "Nova AI Chatbot"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
SYSTEM_PROMPT = """You are Nova, a helpful general-purpose AI assistant.
Answer clearly and accurately. Adapt explanations to the user's level.
For coding questions, explain assumptions and provide runnable examples where useful.
If you are unsure or lack current information, say so rather than inventing facts.
For high-stakes medical, legal, or financial questions, provide general information
and encourage the user to consult a qualified professional.
Use Markdown formatting when it improves readability."""

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_api_key():
    """Read the key from Streamlit secrets first, then environment variables."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GROQ_API_KEY", "")

def prepare_messages(history, new_prompt):
    """Return a bounded conversation context for the API."""
    recent = history[-20:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in recent:
        if item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str):
            messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": new_prompt})
    return messages

st.title("🤖 Nova AI Chatbot")
st.caption("A general-purpose AI assistant built with Python, Streamlit and Groq.")

with st.sidebar:
    st.header("Chat controls")
    st.write("Ask questions, learn concepts, debug code, or brainstorm ideas.")
    model_name = st.text_input(
        "Model ID",
        value=DEFAULT_MODEL,
        help="Use a model ID currently available to your Groq account.",
    ).strip() or DEFAULT_MODEL

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("Example prompts")
    examples = [
        "Explain artificial intelligence in simple words.",
        "Write a Python program to check a prime number.",
        "Explain BFS vs DFS with an example.",
        "Help me prepare for an AI lab viva.",
    ]
    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example
            st.rerun()

    st.divider()
    st.caption("Privacy note: messages sent to the AI provider are processed by that provider. Do not enter passwords, API keys, or other sensitive information.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.messages:
    st.info("Welcome! Type a question below or choose an example prompt from the sidebar.")

prompt = st.chat_input("Message Nova...")
if not prompt and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = ""

if prompt:
    prompt = prompt.strip()
    if not prompt:
        st.warning("Please enter a question.")
    elif len(prompt) > 12000:
        st.warning("Please keep each message under 12,000 characters.")
    else:
        api_key = get_api_key()
        if not api_key:
            st.error(
                "Groq API key not found. Create a key at https://console.groq.com/keys, "
                "then add it to .streamlit/secrets.toml as GROQ_API_KEY. See README.md."
            )
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Nova is thinking..."):
                        client = Groq(api_key=api_key)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=prepare_messages(
                                st.session_state.messages[:-1], prompt
                            ),
                            temperature=0.7,
                            max_tokens=1200,
                        )
                        answer = response.choices[0].message.content or "I couldn't generate a response. Please try again."
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except AuthenticationError:
                    st.error("The API key was rejected. Check your key in .streamlit/secrets.toml.")
                    st.session_state.messages.pop()
                except RateLimitError:
                    st.error("The API rate limit was reached. Wait a little and try again.")
                    st.session_state.messages.pop()
                except APIConnectionError:
                    st.error("Could not connect to the AI service. Check your internet connection and try again.")
                    st.session_state.messages.pop()
                except APIStatusError as exc:
                    st.error(f"The AI service returned an error (HTTP {exc.status_code}). Check the model ID and provider status.")
                    st.session_state.messages.pop()
                except Exception as exc:
                    st.error(f"Unexpected error: {type(exc).__name__}. Check the terminal for details.")
                    st.session_state.messages.pop()

if st.session_state.messages:
    export_data = {
        "app": APP_TITLE,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "messages": st.session_state.messages,
    }
    st.sidebar.download_button(
        "⬇️ Export conversation (JSON)",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name="nova_conversation.json",
        mime="application/json",
        use_container_width=True,
    )
