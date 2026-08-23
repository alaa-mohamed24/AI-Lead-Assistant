import os 
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# if not GOOGLE_API_KEY:
#     raise ValueError ( "GOOGLE_API_KEY is missing in .env file")



TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")