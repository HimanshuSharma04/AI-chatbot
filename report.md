# Nova AI Chatbot — Project Report

**Project title:** Nova AI Chatbot: A General-Purpose Conversational Assistant  
**Technology:** Python, Streamlit, Groq API, Large Language Model (LLM)  
**Student name:** ____________________  
**Roll number:** ____________________  
**Course / Subject:** Artificial Intelligence Lab  
**Institution:** ____________________  
**Submission date:** ____________________

## 1. Abstract

Nova AI Chatbot is a web-based conversational application that accepts natural-language questions and generates responses using a hosted large language model through the Groq API. The user interface is developed with Streamlit and Python. The application supports multi-turn conversation context, example prompts, conversation export, and clear error messages for common API failures. The API credential is kept in a local secrets file or environment variable instead of being hard-coded in the program. The project demonstrates a practical application of natural-language processing and generative AI without requiring the student to train a large model.

## 2. Introduction

Chatbots are software systems that interact with people through text or speech. Traditional rule-based chatbots rely on predefined patterns and responses. Modern AI chatbots can use large language models to interpret prompts and generate contextually relevant text. This project demonstrates a simple API-backed AI chatbot with a browser-based interface.

## 3. Objectives

- Develop a usable general-purpose chatbot interface.
- Connect a Python application to a hosted language model.
- Preserve recent messages to support follow-up questions.
- Handle missing credentials and common API errors gracefully.
- Demonstrate secure handling of API keys.
- Test the application using a repeatable test checklist.

## 4. Tools and technologies

- **Python:** application logic and API calls.
- **Streamlit:** web UI, chat message display, input, sidebar controls, and downloads.
- **Groq Python SDK:** sends chat completion requests to the hosted model.
- **Large language model:** interprets the conversation and generates natural-language responses.
- **JSON:** optional conversation export.
- **Virtual environment:** isolates project dependencies.

## 5. System architecture

```text
+-----------------------+
| User / Web Browser    |
+-----------+-----------+
            |
            v
+-----------------------+
| Streamlit Chat UI     |
| Input / History       |
+-----------+-----------+
            |
            v
+-----------------------+
| Python Application    |
| Prompt + Context      |
| Error Handling        |
+-----------+-----------+
            |
            v
+-----------------------+
| Groq API over HTTPS   |
+-----------+-----------+
            |
            v
+-----------------------+
| Hosted Language Model |
+-----------+-----------+
            |
            v
   Generated response
            |
            v
+-----------------------+
| Streamlit displays it |
+-----------------------+
```

## 6. Working methodology

1. The user enters a question in the Streamlit chat input.
2. The application validates that the message is not empty or excessively long.
3. It loads the API key from Streamlit secrets or an environment variable.
4. It prepares a system instruction, recent conversation messages, and the new user message.
5. The Groq SDK sends a chat completion request to the selected model.
6. The model generates a response.
7. Streamlit displays the response and adds it to the current session history.
8. The user may continue the conversation, clear it, or export the messages as JSON.

## 7. Algorithm

```text
START
  |
Initialize Streamlit interface
  |
Load recent chat history
  |
Receive user prompt
  |
Is prompt valid? ---- No ----> Display validation message
  |
 Yes
  |
Is API key available? -- No --> Show setup instructions
  |
 Yes
  |
Prepare system prompt + recent history + user prompt
  |
Send request to hosted language model
  |
Request successful? ---- No ---> Display suitable error
  |
 Yes
  |
Display and save assistant response in session
  |
Wait for next prompt / clear / export
  |
STOP when application is closed
```

## 8. Implementation details

The main source file is `app.py`. The `get_api_key()` function retrieves credentials from Streamlit secrets or environment variables. The `prepare_messages()` function constructs a bounded conversation context. The API request uses the Groq Python SDK's chat completion interface. Streamlit's `st.chat_message` and `st.chat_input` render the conversational interface. Exception handling covers authentication failures, rate limits, network failures, and API status errors.

## 9. Testing and expected results

| Test | Expected result |
|---|---|
| General knowledge question | Model returns a relevant answer |
| Follow-up question | Recent context is included |
| Coding question | Model returns a programming explanation or example |
| Missing API key | Setup guidance is displayed |
| Invalid key | Authentication error is handled |
| Rate limit reached | User is asked to wait and retry |
| Clear conversation | Session chat history is reset |
| Export conversation | JSON file downloads |
| Invalid model ID | API error is displayed without an unhandled crash |

These are expected results; record actual outcomes after running the tests on your system.

## 10. Security and privacy

The API key must not be hard-coded in the Python source or committed to a public repository. The project excludes `.streamlit/secrets.toml` through `.gitignore`. The app sends the conversation context to the external AI provider for processing. Therefore, users should not enter passwords, private keys, confidential documents, or other sensitive information. A production deployment would also need authentication, abuse controls, logging policies, and stronger privacy review.

## 11. Advantages

- Simple and accessible browser-based interface.
- Uses a hosted language model without local model training.
- Supports contextual follow-up questions.
- Demonstrates API integration and exception handling.
- Can be extended with retrieval-augmented generation, file support, or a database.

## 12. Limitations

- Requires internet access and an API key.
- Free usage limits and model availability depend on the provider.
- Model answers may contain factual errors.
- Chat history is session-based, not stored in a database.
- The starter project does not include user authentication or document retrieval.

## 13. Future scope

Future improvements may include database-backed chat history, user authentication, retrieval-augmented generation (RAG) over class notes, web search, voice interaction, response streaming, multilingual controls, and cloud deployment.

## 14. Conclusion

Nova AI Chatbot demonstrates how a Python application can provide a conversational interface to a hosted large language model. It combines Streamlit for interaction, the Groq SDK for inference requests, and secure credential configuration. The project is suitable as an introductory AI lab demonstration and provides a foundation for more advanced conversational systems.

## 15. References

1. Streamlit Documentation, Chat elements: https://docs.streamlit.io/develop/api-reference/chat
2. Streamlit Documentation, Secrets management: https://docs.streamlit.io/develop/concepts/connections/secrets-management
3. Groq Documentation, Quickstart: https://console.groq.com/docs/quickstart
4. Groq Documentation, API Reference: https://console.groq.com/docs/api-reference
