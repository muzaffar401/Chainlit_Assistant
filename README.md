# 🌟 Chainlit Chatbot - Step by Step Guide 🚀

Welcome to the **Chainlit Chatbot** project! This guide walks you through creating a chatbot using **Chainlit**, **Google Gemini AI**, and **GitHub authentication**. Each step builds upon the previous one, making it easy to follow.

## 🛠️ Prerequisites  

Before starting, make sure you have:

- **Python 3.9+** installed  
- **VS Code or any code editor**  
- **A Google Gemini API Key** (Sign up on Google AI)  
- **A GitHub OAuth app for authentication**  

---

## 🔧 Step 1: Install Required Packages  

To set up the project, install the necessary dependencies using **uv**:

```sh
uv venv .venv  # Create a virtual environment
source .venv/bin/activate  # Activate the virtual environment (Linux/macOS)
.venv\Scripts\activate  # Activate on Windows

uv add google-generativeai chainlit dotenv  # Install required libraries
```

### Explanation:
- `google-generativeai`: Allows us to use Google Gemini AI for responses.  
- `chainlit`: The framework for building chat interfaces in Python.  
- `dotenv`: Loads environment variables from a `.env` file.  

---

## 🔹 Step 1: Create a Simple Chatbot  

This is the most basic chatbot that simply **echoes** whatever the user says.

```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    response = f"You said: {message.content}"
    await cl.Message(content=response).send()
```

📌 **Run the chatbot**:  
```sh
chainlit run chatbot.py
```

---

## 🔹 Step 2: Build a Question-Answer Chatbot  

This chatbot **processes user questions** and generates intelligent responses using **Google Gemini AI**.

```python
import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@cl.on_chat_start
async def handle_chat_start():
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    prompt = message.content
    response = model.generate_content(prompt)
    response_text = response.text if hasattr(response, "text") else ""
    await cl.Message(content=response_text).send()
```

📌 **Run the chatbot**:  
```sh
chainlit run chatbot.py
```

---

## 🔹 Step 3: Add Stateful Chatbot with Authentication  

Now, we will add:
- **Session-based chat memory** to track conversation history.  
- **GitHub OAuth authentication** for secure login.  

```python
import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@cl.oauth_callback
def oauth_callback(provider_id: str, token: str, raw_user_data: Dict[str, str], default_user: cl.User) -> Optional[cl.User]:
    print(f"Provider: {provider_id}")
    print(f"User data: {raw_user_data}")
    return default_user

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    
    formatted_history = [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in history]
    
    response = model.generate_content(formatted_history)
    response_text = response.text if hasattr(response, "text") else ""

    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)

    await cl.Message(content=response_text).send()
```

📌 **Run the chatbot**:  
```sh
chainlit run chatbot.py
```

---

## 📜 Step 4: Configure `chainlit.yaml`  

This file configures authentication and chatbot settings.

```yaml
chainlit: 2.4.1

ui:
  name: "Chainlit Chatbot"
  description: "A Question Answering Stateful chatbot with GitHub authentication."

default_expand_messages: true

auth:
  required: true
  providers: 
    - github

oauth_providers:
  github:
    client_id: ${OAUTH_GITHUB_CLIENT_ID}
    client_secret: ${OAUTH_GITHUB_CLIENT_SECRET}
```

---

## 🔐 Step 5: Configure `.env`  

This file stores **API keys** and **secrets**.

```sh
GEMINI_API_KEY="your-gemini-api-key"
OAUTH_GITHUB_CLIENT_ID="your-client-id"
OAUTH_GITHUB_CLIENT_SECRET="your-client-secret"
CHAINLIT_AUTH_SECRET="your-auth-secret"
```

---

## 🏃 Running the Chatbot  

📌 **To start the chatbot**, run:  
```sh
chainlit run chatbot.py
```

📌 **To use authentication**, set up GitHub OAuth and include credentials in `.env`.  

---

## 🎉 Conclusion  

You have successfully built a **3-step Chainlit chatbot** with:
✔️ **Basic chat functionality**  
✔️ **Google Gemini AI integration**  
✔️ **Session-based chat memory**  
✔️ **GitHub authentication**  

🔗 **Explore More:**  
- [Chainlit Docs](https://docs.chainlit.io/)  
- [Google Gemini AI](https://ai.google.dev/)  

Happy coding! 🚀✨  
