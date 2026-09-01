import json
import os
import streamlit as st
from groq import Groq
from src.ai_lead_assistant.models import Lead

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None


def extract_lead(conversation_history) -> Lead:
    if not client:
        return Lead()

    prompt = f"""
    قم بتحليل المحادثة التالية واستخراج بيانات العميل بتنسيق JSON حصراً:
    المحادثة: {conversation_history}

    قم بإرجاع JSON فقط بالشكل التالي:
    {{
        "name": "اسم العميل أو null",
        "phone": "رقم الهاتف أو null",
        "budget": "الميزانية أو null",
        "location": "المنطقة المفضلة أو null"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        data = json.loads(response.choices[0].message.content)
        return Lead(**data)
    except Exception as e:
        print(f"❌ Extraction Error with Groq: {e}")
        return Lead()