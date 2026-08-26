import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
import streamlit as st
# 1. تحميل الـ .env وتخطي القيم القديمة في النظم
load_dotenv(find_dotenv(), override=True)

api_key = None

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing! Check Streamlit Secrets or .env file.")

# 2. إنشاء الـ Client
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an AI real estate lead assistant.
Your main responsibilities are:
1. Understand the customer's real estate needs.
2. Have a natural and friendly conversation.
3. Collect important lead information.
4. Ask follow-up questions when important information is missing.
5. Never invent information that customer did not provide.
6. Keep the conversation focused on the customer's real estate needs.
"""

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
)

def chat(conversation_history: list, user_message: str) -> str:
    # تحويل الهيستوري بالشكل المتوافق مع SDK الجديدة
    formatted_history = []
    for item in conversation_history:
        role = "model" if item.get("role") in ["model", "assistant"] else "user"
        parts = item.get("parts", [])
        text_content = parts[0].get("text", "") if parts and isinstance(parts[0], dict) else str(parts[0] if parts else "")
        
        formatted_history.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=text_content)]
            )
        )

    # إنشاء جلسة Chat للتعامل مع الـ History
    chat_session = client.chats.create(
        model="gemini-2.5-flash",
        config=config,
        history=formatted_history
    )

    response = chat_session.send_message(user_message)
    ai_response = response.text

    # تحديث الـ conversation_history الأصلية
    conversation_history.append({"role": "user", "parts": [{"text": user_message}]})
    conversation_history.append({"role": "model", "parts": [{"text": ai_response}]})

    return ai_response

