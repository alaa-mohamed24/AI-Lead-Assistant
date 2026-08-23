import os
import streamlit as st
from google import genai
from google.genai.errors import APIError, ClientError
from src.ai_lead_assistant.config import GOOGLE_API_KEY


api_key = st.secrets.get("GEMINI_API_KEY") or GOOGLE_API_KEY or os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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
    formatted_contents = []
    
    
    for msg in conversation_history:
        if isinstance(msg, dict):
            role_val = msg.get("role") or msg.get("sender") or "user"
            role = "user" if role_val in ["user", "human"] else "model"
            
            
            text_val = ""
            if "parts" in msg and isinstance(msg["parts"], list) and len(msg["parts"]) > 0:
                part = msg["parts"][0]
                text_val = part.get("text", "") if isinstance(part, dict) else str(part)
            else:
                text_val = msg.get("content") or msg.get("text") or str(msg)
                
            formatted_contents.append({"role": role, "parts": [{"text": text_val}]})

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted_contents,
            config={
                "system_instruction": SYSTEM_INSTRUCTION
            }
        )
        return response.text
    except (ClientError, APIError) as e:
        print(f"[Gemini API Error]: {e}")
        if getattr(e, 'code', None) == 401 or "401" in str(e):
            return "عذراً، يوجد خطأ في مفتاح الـ API (401 Unauthorized). يرجى التأكد من ضبط GEMINI_API_KEY في Streamlit Secrets."
        elif getattr(e, 'code', None) == 429 or "429" in str(e):
            return "عذراً، تم تجاوز حد الطلبات (Rate Limit). يرجى المحاولة بعد بضع ثوانٍ."
        return "حدث خطأ أثناء التواصل مع سيرفر الذكاء الاصطناعي، يرجى المحاولة مرة أخرى."
    except Exception as e:
        print(f"[Unexpected Exception]: {e}")
        return "Sorry, I am receiving too many requests right now. Please try sending your message again in a few seconds."

def chat(conversation_history, user_message):
    
    conversation_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    # طلب الرد من Gemini
    ai_response = ask_gemini(conversation_history)
    
    
    conversation_history.append({
        "role": "model",
        "parts": [{"text": ai_response}]
    })
    
    return ai_response