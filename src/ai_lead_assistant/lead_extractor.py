import time
import os
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError
from src.ai_lead_assistant.models import Lead

def get_api_key_safe():
    """جلب المفتاح مع دعم Streamlit Secrets و .env"""
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def extract_lead(conversation_history):
    api_key = get_api_key_safe()
    if not api_key:
        print("[Warning] No API key found in extract_lead")
        return Lead()

    client = genai.Client(api_key=api_key, vertexai=False)

    conversation_text = ""
    for message in conversation_history:
        if isinstance(message, dict):
            role = message.get("role") or message.get("sender") or "user"
            text = ""
            if "parts" in message and isinstance(message["parts"], list) and len(message["parts"]) > 0:
                part = message["parts"][0]
                text = part.get("text", "") if isinstance(part, dict) else str(part)
            else:
                text = message.get("content") or message.get("text") or str(message)
            
            conversation_text += f"{role}: {text}\n"

    prompt = f"""
Extract the real estate lead information from the entire customer conversation below.

Customer conversation:
{conversation_text}

Important instructions:
1. Analyze the entire conversation, not only the last message.
2. Combine information provided by the customer across different messages.
3. If the customer mentioned a piece of information earlier in the conversation, keep it in the final Lead.
4. Do not remove previously provided information just because it is not mentioned in the latest message.
5. Only extract information that the customer actually provided.
6. Do not invent or assume any information.
7. If a piece of information was never provided, leave it empty.

Return the extracted information according to the Lead model.
"""

    time.sleep(1)

    try:
        # ضبط الإعدادات باستخدام types المعتمدة من google-genai
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Lead,
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config
        )
        return Lead.model_validate_json(response.text)
    except Exception as e:
        print(f"[Warning] Failed to extract lead: {e}")
        return Lead()