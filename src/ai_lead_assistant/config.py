import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_api_key():
    key = None
    try:
        key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
    
    if not key:
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if key:
        return str(key).strip().strip('"').strip("'")
    return None

GOOGLE_API_KEY = get_api_key()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")