import os
import streamlit as st
from google import genai
from google.genai.errors import APIError, ClientError
from src.ai_lead_assistant.config import get_api_key

SYSTEM_INSTRUCTION = """
you are an AI estate lead assistant .
your main responsibities are :
1. understand the customer's real estate needs.
2. have a natural and friendly conversation.
3. collect important lead information.
4. ask follow-up questions when important information is missing.
5. never invent information that customer did not provide.
6. keep the conversation focused on the customer's real estate needs.
"""


def ask_gemini(conversation_history):
    
    api_key = get_api_key()
    if not api_key:
        return "ERROR: GEMINI_API_KEY is missing in Streamlit Secrets!"

    client = genai.Client(api_key=api_key)

    formatted_contents = []
    for msg in conversation_history:
        if isinstance(msg, dict):
            role_val = msg.get("role") or msg.get("sender") or "user"
            role = "user" if role_val in ["user", "human"] else "model"

            text_val = ""
            if (
                "parts" in msg
                and isinstance(msg["parts"], list)
                and len(msg["parts"]) > 0
            ):
                part = msg["parts"][0]
                text_val = (
                    part.get("text", "") if isinstance(part, dict) else str(part)
                )
            else:
                text_val = msg.get("content") or msg.get("text") or str(msg)

            formatted_contents.append(
                {"role": role, "parts": [{"text": text_val}]}
            )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_contents,
            config={"system_instruction": SYSTEM_INSTRUCTION},
        )
        return response.text
    except Exception as e:
        print(f"[Gemini API Exception Caught]: {e}")
        return "Sorry, I am receiving too many requests right now or key is invalid. Please try again in a few seconds."


def chat(conversation_history, user_message):
    conversation_history.append(
        {"role": "user", "parts": [{"text": user_message}]}
    )

    ai_response = ask_gemini(conversation_history)

    conversation_history.append(
        {"role": "model", "parts": [{"text": ai_response}]}
    )

    return ai_response