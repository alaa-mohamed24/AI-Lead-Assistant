import sys
from pathlib import Path

file_path = Path(__file__).resolve()
root_path = file_path.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import pandas as pd
import streamlit as st
from src.ai_lead_assistant.database import get_leads
from src.ai_lead_assistant.main import handel_message

st.set_page_config(
    page_title="Real Estate AI Lead Assistant", page_icon="🏢", layout="wide"
)

st.title("🏢 Real Estate AI Lead Assistant")

# تهيئة المتغيرات في session_state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_lead" not in st.session_state:
    st.session_state.current_lead = None

if "current_lead_id" not in st.session_state:
    st.session_state.current_lead_id = None

if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = {"score": 0, "classification": "N/A"}

tab1, tab2 = st.tabs(["💬 Chat Simulator", "📊 Leads Dashboard"])

with tab1:
    col_chat, col_info = st.columns([2, 1])

    with col_chat:
        st.subheader("Customer Chat")

        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_input := st.chat_input("Type Your Message here...."):
            
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.conversation_history.append({"role": "user", "content": user_input})

            with st.spinner("AI is thinking & analyzing...."):
                
                ai_response, lead, analysis, lead_id = handel_message(
                    st.session_state.conversation_history,
                    user_input,
                    existing_lead_id=st.session_state.current_lead_id
                )

                
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})

                
                st.session_state.current_lead = lead
                st.session_state.current_lead_id = lead_id
                st.session_state.current_analysis = (
                    analysis
                    if isinstance(analysis, dict)
                    else {"score": 0, "classification": "N/A"}
                )

            st.rerun()

    with col_info:
        st.subheader("📌 Extracted Lead Details")

        analysis = st.session_state.get("current_analysis") or {
            "score": 0,
            "classification": "N/A",
        }
        score = analysis.get("score", 0) if isinstance(analysis, dict) else 0
        classification = (
            str(
                analysis.get("classification", "N/A")
                if isinstance(analysis, dict)
                else "N/A"
            )
            .strip()
            .upper()
        )

        # عرض التقييم بألوان مختلفة حسب التصنيف
        if classification == "HOT":
            st.error(f"🔥 Score: {score}/100 ({classification})")
        elif classification == "WARM":
            st.warning(f"⚡ Score: {score}/100 ({classification})")
        else:
            st.info(f"❄️ Score: {score}/100 ({classification})")

        # --- عرض البيانات الاستخراجية الحالية ---
        lead = st.session_state.get("current_lead", None)
        lead_dict = {}
        if lead:
            if hasattr(lead, "model_dump"):
                lead_dict = lead.model_dump(mode="json")
            elif isinstance(lead, dict):
                lead_dict = lead

        def clean_val(val):
            if val is None or "UNKNOWN" in str(val).upper() or str(val).strip() == "":
                return "---"
            return str(val)

        st.markdown("---")
        st.markdown(f"**🆔 Lead ID:** {clean_val(st.session_state.get('current_lead_id'))}")
        st.markdown(f"**👤 Name:** {clean_val(lead_dict.get('name'))}")
        st.markdown(f"**📞 Phone:** {clean_val(lead_dict.get('phone'))}")
        st.markdown(f"**🏠 Property:** {clean_val(lead_dict.get('property_type'))}")
        st.markdown(f"**📍 Location:** {clean_val(lead_dict.get('location'))}")
        st.markdown(f"**💰 Budget:** {clean_val(lead_dict.get('budget'))}")
        st.markdown(f"**🛏️ Bedrooms:** {clean_val(lead_dict.get('bedrooms'))}")
        st.markdown(f"**🎨 Finishing:** {clean_val(lead_dict.get('finishing'))}")
        st.markdown(f"**⏱️ Timeline:** {clean_val(lead_dict.get('timeline'))}")

        st.markdown("---")
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.session_state.current_lead = None
            st.session_state.current_lead_id = None
            st.session_state.current_analysis = {
                "score": 0,
                "classification": "N/A",
            }
            st.rerun()

with tab2:
    st.subheader("📊 Saved Leads Tracker")

    leads_data = get_leads()

    if leads_data:
        df = pd.DataFrame(leads_data)

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Leads", len(df))
        if "classification" in df.columns:
            m2.metric(
                "Hot Leads 🔥",
                len(df[df["classification"].astype(str).str.lower() == "hot"]),
            )
            m3.metric(
                "Warm Leads ⚡",
                len(df[df["classification"].astype(str).str.lower() == "warm"]),
            )

        st.markdown("---")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No leads saved in database yet.")
