import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from groq import Groq

# 1. تحميل الـ .env
load_dotenv(find_dotenv(), override=True)

# 2. جلب المفتاح بأمان من st.secrets أو os.getenv
api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Check Streamlit Secrets or .env file.")

# 3. إنشاء الـ Client الخاص بـ Groq
client = Groq(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an AI real estate lead assistant.
Your main responsibilities are:
1. Understand the customer's real estate needs.
2. Have a natural, polite, and friendly conversation.
3. Collect important lead information (Name, Phone, Property Type, Location, Budget, Bedrooms, Finishing, Timeline, Intent).
4. Ask clear follow-up questions when important information is missing.
5. Never invent information that customer did not provide.
6. Keep the conversation focused on the customer's real estate needs.
"""

def chat(conversation_history: list, user_message: str) -> str:
    try:
        # بناء قائمة الرسائل المتوافقة مع Groq
        messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]

        # تحويل الـ History القديم إلى صيغة Groq
        for item in conversation_history:
            role = "assistant" if item.get("role") in ["model", "assistant"] else "user"
            
            # استخراج النص سواء كان القالب القديم (parts) أو الجديد (content)
            content = ""
            if "content" in item:
                content = item["content"]
            elif "parts" in item and item["parts"]:
                part = item["parts"][0]
                content = part.get("text", "") if isinstance(part, dict) else str(part)

            if content:
                messages.append({"role": role, "content": content})

        # إضافة رسالة المستخدم الحالية
        messages.append({"role": "user", "content": user_message})

        # إرسال الطلب لموديل Llama 3.1 الفائق السرعة
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )

        ai_response = completion.choices[0].message.content

        # تحديث الـ conversation_history الأصلية بنفس النمط الموحد (content)
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        return ai_response

    except Exception as e:
        print(f"❌ [Groq Chat Error]: {e}")
        return "Sorry, I am having trouble processing your request right now. Please try again."

