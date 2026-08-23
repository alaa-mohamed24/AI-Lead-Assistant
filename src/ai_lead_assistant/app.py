
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
from src.ai_lead_assistant.sheets import get_worksheet

st.set_page_config(
    page_title="Real Estate AI Lead Assistant", page_icon="🏢", layout="wide"
)

st.title("🏢 Real Estate AI Lead Assistant")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_lead" not in st.session_state:
    st.session_state.current_lead = None

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
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.write(user_input)

            with st.spinner("AI is thinking & analyzing...."):
                ai_response, lead, analysis, lead_id = handel_message(
                    st.session_state.conversation_history, user_input
                )

                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_response}
                )

                # تحديث الـ States مع حماية القيمة
                st.session_state.current_lead = lead
                st.session_state.current_analysis = (
                    analysis
                    if isinstance(analysis, dict)
                    else {"score": 0, "classification": "N/A"}
                )

            with st.chat_message("assistant"):
                st.write(ai_response)
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

        
        if classification == "HOT":
            st.error(f"🔥 Score: {score}/100 ({classification})")
        elif classification == "WARM":
            st.warning(f"⚡ Score: {score}/100 ({classification})")
        else:
            st.info(f"❄️ Score: {score}/100 ({classification})")

        
        lead = st.session_state.get("current_lead", None)
        if lead:
            lead_dict = (
                lead.model_dump()
                if hasattr(lead, "model_dump")
                else (dict(lead) if isinstance(lead, dict) else {})
            )

            st.markdown("---")
            st.markdown(f"**👤 Name:** {lead_dict.get('name') or '---'}")
            st.markdown(f"**📞 Phone:** {lead_dict.get('phone') or '---'}")
            st.markdown(
                f"**🏠 Property:** {lead_dict.get('property_type') or '---'}"
            )
            st.markdown(
                f"**📍 Location:** {lead_dict.get('location') or '---'}"
            )
            st.markdown(f"**💰 Budget:** {lead_dict.get('budget') or '---'}")
            st.markdown(
                f"**🛏️ Bedrooms:** {lead_dict.get('bedrooms') or '---'}"
            )
            st.markdown(
                f"**🎨 Finishing:** {lead_dict.get('finishing') or '---'}"
            )
            st.markdown(
                f"**⏱️ Timeline:** {lead_dict.get('timeline') or '---'}"
            )
        else:
            st.write("Start a conversation to see extracted details.")

        if st.button("🔄 Reset Conversation"):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.session_state.current_lead = None
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
                len(
                    df[
                        df["classification"].astype(str).str.lower() == "warm"
                    ]
                ),
            )

        st.markdown("---")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No leads saved in database yet.")
